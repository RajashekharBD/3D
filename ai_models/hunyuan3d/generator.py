import gc
import torch
import numpy as np
import trimesh
from PIL import Image
from backend.app.core.settings import settings
from backend.app.utils.logger import logger

@torch.inference_mode()
def generate_shape(image_path: str, pipeline, steps: int = 10, guidance_scale: float = 5.5, offload: bool = True) -> trimesh.Trimesh:
    """Generates 3D mesh geometry from an RGBA image.
    
    If running in mock mode, procedurally extrudes/scales a primitive watertight mesh.
    Otherwise, runs a manual step-by-step CPU/GPU offloaded inference flow to fit in low VRAM if offload=True.
    """
    image = Image.open(image_path).convert("RGBA")
    
    if pipeline == "mock_pipeline":
        logger.info("Executing procedural 3D mesh generation (fallback).")
        # Extract alpha mask
        alpha = np.array(image.split()[-1])
        y_indices, x_indices = np.where(alpha > 0)
        
        # Default scaling factors
        scale_x = 1.0
        scale_y = 1.0
        scale_z = 1.0
        
        if len(y_indices) > 0:
            ymin, ymax = y_indices.min(), y_indices.max()
            xmin, xmax = x_indices.min(), x_indices.max()
            w = xmax - xmin
            h = ymax - ymin
            # Compute dimension ratio relative to typical image size
            scale_x = max(0.1, w / 100.0)
            scale_y = max(0.1, h / 100.0)
            scale_z = max(0.1, (w + h) / 200.0)
            
        # Create a watertight icosphere
        mesh = trimesh.creation.icosphere(subdivisions=3, radius=0.5)
        # Apply scaling based on bounding box
        mesh.apply_scale([scale_x, scale_y, scale_z])
        return mesh
        
    # Resize input image to the lowest supported resolution to save VRAM
    target_res = 256
    logger.info(f"Resizing input image from {image.size} to ({target_res}, {target_res})")
    image = image.resize((target_res, target_res), Image.Resampling.LANCZOS)
    
    octree_res = getattr(settings.hunyuan3d, "octree_resolution", 128)

    if not offload:
        logger.info("Executing shape generation directly on GPU (no manual CPU offloading)...")
        outputs = pipeline(
            image=image,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            octree_resolution=octree_res,
            num_chunks=2000,
            enable_pbar=False
        )
        mesh = outputs
        while isinstance(mesh, list):
            if len(mesh) == 0:
                raise ValueError("Pipeline returned an empty mesh list.")
            mesh = mesh[0]
        return mesh

    logger.info("Executing Hunyuan3D-2 shape generation pipeline with low-memory sequential offloading...")
    
    # 2. Get device and dtype details
    device = pipeline.device
    dtype = pipeline.dtype
    
    # Enforce everything starts on CPU to prevent initial spike
    logger.info("Moving all shape pipeline components to CPU...")
    if hasattr(pipeline, "conditioner") and pipeline.conditioner is not None:
        pipeline.conditioner.to("cpu")
    if hasattr(pipeline, "model") and pipeline.model is not None:
        pipeline.model.to("cpu")
    if hasattr(pipeline, "vae") and pipeline.vae is not None:
        pipeline.vae.to("cpu")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    # Step A: Run SingleImageEncoder (conditioner) on GPU
    logger.info("Offloading Phase 1: Moving conditioner to GPU...")
    pipeline.conditioner.to(device)
    
    do_classifier_free_guidance = guidance_scale >= 0 and not (
        hasattr(pipeline.model, 'guidance_embed') and
        pipeline.model.guidance_embed is True
    )
    
    cond_inputs = pipeline.prepare_image(image)
    img_tensor = cond_inputs.pop('image')
    
    cond = pipeline.encode_cond(
        image=img_tensor,
        additional_cond_inputs=cond_inputs,
        do_classifier_free_guidance=do_classifier_free_guidance,
        dual_guidance=False,
    )
    batch_size = img_tensor.shape[0]
    
    # Immediately move conditioner back to CPU and clear cache
    logger.info("Offloading Phase 1: Moving conditioner back to CPU...")
    pipeline.conditioner.to("cpu")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    # Step B: Run Hunyuan3DDiT (denoiser model) on GPU
    logger.info("Offloading Phase 2: Moving denoiser model to GPU...")
    pipeline.model.to(device)
    
    # Retrieve timesteps and prepare latents
    from hy3dgen.shapegen.pipelines import retrieve_timesteps
    sigmas = np.linspace(0, 1, steps)
    timesteps, steps = retrieve_timesteps(
        pipeline.scheduler,
        steps,
        device,
        sigmas=sigmas,
    )
    latents = pipeline.prepare_latents(batch_size, dtype, device, None)
    
    guidance = None
    if hasattr(pipeline.model, 'guidance_embed') and pipeline.model.guidance_embed is True:
        guidance = torch.tensor([guidance_scale] * batch_size, device=device, dtype=dtype)
        
    logger.info(f"Running diffusion sampling loop for {steps} steps...")
    for i, t in enumerate(timesteps):
        if do_classifier_free_guidance:
            latent_model_input = torch.cat([latents] * 2)
        else:
            latent_model_input = latents

        timestep = t.expand(latent_model_input.shape[0]).to(latents.dtype) / pipeline.scheduler.config.num_train_timesteps
        
        # Run forward pass
        noise_pred = pipeline.model(latent_model_input, timestep, cond, guidance=guidance)

        if do_classifier_free_guidance:
            noise_pred_cond, noise_pred_uncond = noise_pred.chunk(2)
            noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_cond - noise_pred_uncond)

        outputs = pipeline.scheduler.step(noise_pred, t, latents)
        latents = outputs.prev_sample
        
    # Immediately move denoiser back to CPU and clear cache
    logger.info("Offloading Phase 2: Moving denoiser model back to CPU...")
    pipeline.model.to("cpu")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

    # Step C: Run ShapeVAE (vae decoder) on GPU
    logger.info("Offloading Phase 3: Moving VAE to GPU...")
    pipeline.vae.to(device)
    
    octree_res = getattr(settings.hunyuan3d, "octree_resolution", 128)
    logger.info(f"Exporting mesh with octree_resolution={octree_res}")
    
    # Run vae decoding and export to trimesh
    mesh_outputs = pipeline._export(
        latents,
        output_type="trimesh",
        box_v=1.01,
        mc_level=0.0,
        num_chunks=2000, # Lowered to fit in VRAM
        octree_resolution=octree_res,
        mc_algo=None,
        enable_pbar=False,
    )
    
    # Move VAE back to CPU and perform final GPU cleanup
    logger.info("Offloading Phase 3: Moving VAE back to CPU...")
    pipeline.vae.to("cpu")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        
    mesh = mesh_outputs
    while isinstance(mesh, list):
        if len(mesh) == 0:
            raise ValueError("Pipeline returned an empty mesh list.")
        mesh = mesh[0]
    return mesh

@torch.inference_mode()
def generate_texture(image_path: str, mesh: trimesh.Trimesh, pipeline, resolution: int = 256) -> trimesh.Trimesh:
    """Generates PBR texture map from RGBA image and applies it to the mesh.
    
    If running in mock mode, procedurally maps a solid color texture onto the mesh.
    """
    image = Image.open(image_path).convert("RGBA")
    
    if pipeline == "mock_pipeline":
        logger.info("Executing procedural 3D texture mapping (fallback).")
        img_np = np.array(image)
        mask = img_np[:, :, 3] > 0
        if mask.any():
            avg_color = img_np[mask, :3].mean(axis=0).astype(int)
            color = (int(avg_color[0]), int(avg_color[1]), int(avg_color[2]))
        else:
            color = (255, 0, 0) # Fallback red
            
        texture_img = Image.new("RGB", (resolution, resolution), color=color)
        
        # Calculate spherical UV coordinates
        vertices = mesh.vertices
        x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]
        r = np.sqrt(x**2 + y**2 + z**2)
        r = np.where(r == 0, 1e-6, r)
        u = 0.5 + np.arctan2(z, x) / (2 * np.pi)
        v = 0.5 - np.arcsin(y / r) / np.pi
        uv = np.stack([u, v], axis=1)
        
        material = trimesh.visual.material.SimpleMaterial(image=texture_img)
        mesh.visual = trimesh.visual.TextureVisuals(uv=uv, material=material)
        return mesh

    logger.info("Executing Hunyuan3D-2 paint pipeline texture synthesis...")
    # Resize the image to low resolution to save memory
    logger.info(f"Resizing input image from {image.size} to ({resolution}, {resolution})")
    image = image.resize((resolution, resolution), Image.Resampling.LANCZOS)
    
    # Override configuration resolutions dynamically to save memory
    if hasattr(pipeline, "config"):
        pipeline.config.render_size = resolution
        pipeline.config.texture_size = resolution

    # Run the patched call that runs components sequentially
    textured_mesh = pipeline(mesh, image=image)
    
    # Final cleanup
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        
    return textured_mesh

import gc
import torch
from PIL import Image
import numpy as np
from backend.app.core.settings import settings
from backend.app.utils.logger import logger

# Try importing the official Hunyuan3D-2 library
try:
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    from hy3dgen.texgen import Hunyuan3DPaintPipeline
    from hy3dgen.texgen.utils.uv_warp_utils import mesh_uv_wrap
    HAS_HY3DGEN = True
except ImportError:
    HAS_HY3DGEN = False

def optimize_diffusers_pipeline(pipe):
    """Applies all possible memory saving optimizations to a Diffusers pipeline."""
    if pipe is None:
        return
    
    # 1. Enable attention slicing
    if settings.hunyuan3d.attention_slicing:
        try:
            logger.info("Enabling attention slicing for Diffusers pipeline...")
            pipe.enable_attention_slicing()
        except Exception as e:
            logger.warning(f"Could not enable attention slicing: {e}")
    
    # 2. Enable VAE slicing
    if settings.hunyuan3d.vae_slicing:
        try:
            logger.info("Enabling VAE slicing for Diffusers pipeline...")
            pipe.enable_vae_slicing()
        except Exception as e:
            logger.warning(f"Could not enable VAE slicing: {e}")
        
    # 3. Enable VAE tiling
    if settings.hunyuan3d.vae_tiling:
        try:
            logger.info("Enabling VAE tiling for Diffusers pipeline...")
            pipe.enable_vae_tiling()
        except Exception as e:
            logger.warning(f"Could not enable VAE tiling: {e}")
        
    # 4. Enable xformers memory efficient attention if available
    try:
        pipe.enable_xformers_memory_efficient_attention()
        logger.info("Enabled xformers memory efficient attention.")
    except Exception:
        pass

    # 5. Enable CPU offloading
    if settings.hunyuan3d.sequential_cpu_offload:
        try:
            logger.info("Enabling sequential CPU offloading for Diffusers pipeline...")
            pipe.enable_sequential_cpu_offload()
        except Exception as e:
            logger.warning(f"Could not enable sequential CPU offload: {e}")
    elif settings.hunyuan3d.cpu_offload:
        try:
            logger.info("Enabling model CPU offloading for Diffusers pipeline...")
            pipe.enable_model_cpu_offload()
        except Exception as e:
            logger.warning(f"Could not enable model CPU offload: {e}")

def patch_texture_pipeline(pipeline, target_device):
    """Patches the Hunyuan3DPaintPipeline to load and unload models sequentially to conserve memory."""
    # Prevent default simultaneous loading
    def custom_load_models(self):
        self.models = {}
    
    pipeline.load_models = custom_load_models.__get__(pipeline, pipeline.__class__)
    pipeline.models = {}
    
    # Overwrite __call__ to load, run, and unload each sub-model sequentially
    def custom_call(self, mesh, image):
        self.config.device = target_device
        
        if not isinstance(image, list):
            image = [image]

        images_prompt = []
        for i in range(len(image)):
            if isinstance(image[i], str):
                image_prompt = Image.open(image[i])
            else:
                image_prompt = image[i]
            images_prompt.append(image_prompt)
            
        images_prompt = [self.recenter_image(image_prompt) for image_prompt in images_prompt]

        # Stage 1: Load and run delight_model
        logger.info("Texture Stage 1: Loading delight_model...")
        from hy3dgen.texgen.utils.dehighlight_utils import Light_Shadow_Remover
        delight_model = Light_Shadow_Remover(self.config)
        
        if hasattr(delight_model, 'pipeline'):
            optimize_diffusers_pipeline(delight_model.pipeline)
            if target_device == 'cpu':
                delight_model.pipeline = delight_model.pipeline.to('cpu')
            
        logger.info("Texture Stage 1: Running delight_model inference...")
        images_prompt = [delight_model(image_prompt) for image_prompt in images_prompt]
        
        # Unload delight_model
        logger.info("Texture Stage 1: Unloading delight_model from memory...")
        del delight_model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

        mesh = mesh_uv_wrap(mesh)
        self.render.load_mesh(mesh)

        selected_camera_elevs, selected_camera_azims, selected_view_weights = \
            self.config.candidate_camera_elevs, self.config.candidate_camera_azims, self.config.candidate_view_weights

        normal_maps = self.render_normal_multiview(
            selected_camera_elevs, selected_camera_azims, use_abs_coor=True)
        position_maps = self.render_position_multiview(
            selected_camera_elevs, selected_camera_azims)

        camera_info = [(((azim // 30) + 9) % 12) // {-20: 1, 0: 1, 20: 1, -90: 3, 90: 3}[
            elev] + {-20: 0, 0: 12, 20: 24, -90: 36, 90: 40}[elev] for azim, elev in
                       zip(selected_camera_azims, selected_camera_elevs)]
                       
        # Stage 2: Load and run multiview_model
        logger.info("Texture Stage 2: Loading multiview_model...")
        from hy3dgen.texgen.utils.multiview_utils import Multiview_Diffusion_Net
        multiview_model = Multiview_Diffusion_Net(self.config)
        
        if hasattr(multiview_model, 'pipeline'):
            optimize_diffusers_pipeline(multiview_model.pipeline)
            if target_device == 'cpu':
                multiview_model.pipeline = multiview_model.pipeline.to('cpu')
            
        logger.info("Texture Stage 2: Running multiview_model inference...")
        multiviews = multiview_model(images_prompt, normal_maps + position_maps, camera_info)
        
        # Unload multiview_model
        logger.info("Texture Stage 2: Unloading multiview_model from memory...")
        del multiview_model
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

        for i in range(len(multiviews)):
            multiviews[i] = multiviews[i].resize(
                (self.config.render_size, self.config.render_size))

        texture, mask = self.bake_from_multiview(multiviews,
                                                 selected_camera_elevs, selected_camera_azims, selected_view_weights,
                                                 method=self.config.merge_method)

        mask_np = (mask.squeeze(-1).cpu().numpy() * 255).astype(np.uint8)
        texture = self.texture_inpaint(texture, mask_np)

        self.render.set_texture(texture)
        textured_mesh = self.render.save_mesh()

        return textured_mesh

    pipeline.__class__.__call__ = custom_call

def load_hunyuan3d_model(model_type: str = "shape", device: str = None):
    """Loads Hunyuan3D-2 pipeline based on model_type ('shape' or 'texture') with options for low memory.
    
    If hy3dgen is not installed, returns a fallback mock pipeline.
    """
    if not HAS_HY3DGEN:
        logger.warning(f"hy3dgen library not found. Initialising {model_type} pipeline in fallback mock mode.")
        return "mock_pipeline", None

    if device is None:
        device = settings.hunyuan3d.shape_device if hasattr(settings.hunyuan3d, "shape_device") else "cuda"
    
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    logger.info(f"Loading Hunyuan3D-2 {model_type} pipeline onto device: {device}...")
    try:
        dtype = torch.float16 if settings.hunyuan3d.use_fp16 else torch.float32
        
        if model_type == "shape":
            # Load Shape Generation Pipeline using Diffusers-compatible parameters
            pipeline = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
                'tencent/Hunyuan3D-2',
                device=device,
                dtype=dtype
            )
            # Default shape model: do not move full pipeline to device immediately if we offload sequentially.
            # But the pipeline initialization class automatically calls to(device, dtype) in __init__.
            # We can still keep the pipeline object and manage the offloads during inference.
            
        elif model_type == "texture":
            # Patch the Hunyuan3DPaintPipeline class BEFORE calling from_pretrained to prevent dual model loading
            Hunyuan3DPaintPipeline.load_models = lambda self: setattr(self, "models", {})
            
            # Load Texture Synthesis Pipeline
            pipeline = Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')
            patch_texture_pipeline(pipeline, device)
        else:
            raise ValueError(f"Unknown model_type: {model_type}")

        return pipeline, None
    except Exception as e:
        logger.error(f"Failed to load Hunyuan3D-2 {model_type} model: {e}. Falling back to mock mode.")
        return "mock_pipeline", None

def unload_hunyuan3d_model(pipeline):
    """Safely unloads Hunyuan3D-2 and clears CUDA cache."""
    if pipeline is not None and pipeline != "mock_pipeline":
        logger.info("Unloading Hunyuan3D-2 pipeline...")
        # Clear attributes inside the pipeline if any
        if hasattr(pipeline, "to"):
            try:
                pipeline.to("cpu")
            except Exception:
                pass
        
        # Specific model unload to prevent memory leak
        if hasattr(pipeline, "models"):
            pipeline.models.clear()
        if hasattr(pipeline, "model"):
            del pipeline.model
        if hasattr(pipeline, "vae"):
            del pipeline.vae
        if hasattr(pipeline, "conditioner"):
            del pipeline.conditioner
        del pipeline
        
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

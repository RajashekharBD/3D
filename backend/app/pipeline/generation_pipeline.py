import os
import time
import json
import gc
import trimesh
import torch
import psutil
from backend.app.core.settings import settings
from backend.app.utils.logger import logger
from ai_models.hunyuan3d.loader import load_hunyuan3d_model, unload_hunyuan3d_model
from ai_models.hunyuan3d.generator import generate_shape, generate_texture
from backend.app.utils.artifacts_manager import artifacts_manager

def get_memory_stats():
    """Returns a dictionary containing current GPU and CPU memory statistics."""
    stats = {}
    if torch.cuda.is_available():
        stats["allocated_mb"] = torch.cuda.memory_allocated() / (1024 * 1024)
        stats["max_allocated_mb"] = torch.cuda.max_memory_allocated() / (1024 * 1024)
        stats["reserved_mb"] = torch.cuda.memory_reserved() / (1024 * 1024)
    else:
        stats["allocated_mb"] = 0
        stats["max_allocated_mb"] = 0
        stats["reserved_mb"] = 0
    # CPU memory usage
    vm = psutil.virtual_memory()
    stats["cpu_ram_used_mb"] = (vm.total - vm.available) / (1024 * 1024)
    return stats

def log_memory_status(prefix=""):
    """Helper to write memory metrics to the logger."""
    stats = get_memory_stats()
    logger.info(
        f"[{prefix}] GPU Allocated: {stats['allocated_mb']:.2f} MB, "
        f"GPU Peak: {stats['max_allocated_mb']:.2f} MB, "
        f"GPU Reserved: {stats['reserved_mb']:.2f} MB | "
        f"CPU RAM Used: {stats['cpu_ram_used_mb']:.2f} MB"
    )

def cleanup_memory():
    """Performs aggressive memory cleanups by deleting variables, invoking GC, and freeing caches."""
    logger.info("Executing GPU and CPU memory cleanup...")
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
        torch.cuda.reset_peak_memory_stats()

def run_shape_generation_pipeline(job_id: str, rgba_path: str) -> dict:
    """Executes Stage 5 of the pipeline: 3D Shape Generation (Phase 14).
    
    Loads Hunyuan3D-2, generates a watertight untextured 3D mesh,
    validates geometry elements, saves outputs/<job_id>/model.glb, and unloads model.
    Implements a progressive retry strategy with automatic CPU fallback.
    """
    start_time = time.time()
    logger.info(f"Starting Hunyuan3D-2 Shape Generation for Job ID: {job_id}")
    
    # Resolve job directory paths
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    glb_dest_path = os.path.join(job_dir, "model.glb")
    
    # Progressive retry configurations:
    # 1. Sequential GPU: manual CPU/GPU offloading (fastest for 4GB, stays under threshold)
    # 2. Lower-Res GPU: lower octree resolution (slower, saves more VRAM)
    # 3. Minimum GPU: minimum inference steps (5 steps) and lowest octree
    # 4. CPU Fallback: minimum steps and lowest octree on CPU
    tries = [
        {"device": "cuda", "steps": settings.hunyuan3d.shape_steps, "octree_res": settings.hunyuan3d.octree_resolution, "offload": True},
        {"device": "cuda", "steps": settings.hunyuan3d.shape_steps, "octree_res": 96, "offload": True},
        {"device": "cuda", "steps": 5, "octree_res": 96, "offload": True},
        {"device": "cpu", "steps": 5, "octree_res": 96, "offload": True}
    ]
    
    last_error = None
    for attempt, config in enumerate(tries):
        device = config["device"]
        steps = config["steps"]
        octree_res = config["octree_res"]
        offload = config["offload"]
        
        # Apply temporary settings
        settings.hunyuan3d.octree_resolution = octree_res
        
        logger.info(f"Shape Gen Attempt {attempt + 1}/{len(tries)}: device={device.upper()}, steps={steps}, octree_res={octree_res}, offload={offload}")
        log_memory_status(f"Before Shape Gen Attempt {attempt + 1}")
        
        pipeline = None
        try:
            # Step 1: Load Hunyuan3D-2 model
            logger.info("Loading Hunyuan3D-2 shape generation model...")
            pipeline, _ = load_hunyuan3d_model(model_type="shape", device=device)
            
            # Step 2: Execute shape generation
            guidance_scale = settings.hunyuan3d.guidance_scale
            logger.info(f"Generating 3D mesh with steps={steps}, guidance={guidance_scale}")
            
            mesh = generate_shape(rgba_path, pipeline, steps=steps, guidance_scale=guidance_scale, offload=offload)
            
            # Step 3: Validate geometry elements
            if mesh is None or not isinstance(mesh, trimesh.Trimesh):
                raise ValueError("Generated output is not a valid trimesh.Trimesh object.")
                
            vertex_count = len(mesh.vertices)
            face_count = len(mesh.faces)
            
            logger.info(f"Generated mesh properties: Vertices={vertex_count}, Faces={face_count}")
            if vertex_count == 0 or face_count == 0:
                raise ValueError(f"Generated mesh contains empty geometry elements: Vertices={vertex_count}, Faces={face_count}")
                
            # Step 4: Save the mesh in GLB format
            mesh.export(glb_dest_path, file_type="glb")
            logger.info(f"Saved untextured 3D model to: {glb_dest_path}")
            
            # Step 5: Unload model to recover VRAM immediately
            logger.info("Unloading Hunyuan3D-2 shape generation model...")
            unload_hunyuan3d_model(pipeline)
            pipeline = None
            
            # Step 6: Update result.json via artifacts_manager
            artifacts_manager.add_file_artifact(job_id, "model", glb_dest_path, "model.glb")
            artifacts_manager.add_completed_phase(job_id, "shape_generation")
            
            # Append detailed mesh metadata to result.json
            result_json_path = os.path.join(job_dir, "result.json")
            if os.path.exists(result_json_path):
                try:
                    with open(result_json_path, "r") as f:
                        res_data = json.load(f)
                    res_data["mesh_metadata"] = {
                        "vertex_count": vertex_count,
                        "face_count": face_count,
                        "generation_time_sec": float(time.time() - start_time)
                    }
                    with open(result_json_path, "w") as f:
                        json.dump(res_data, f, indent=4)
                except Exception as js_err:
                    logger.error(f"Failed to append mesh metadata to result.json: {js_err}")
                    
            # Update metadata JSON file
            metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r") as f:
                        meta = json.load(f)
                    meta["stage"] = "Hunyuan3D-2 Shape Generation"
                    meta["mesh_path"] = glb_dest_path
                    meta["vertex_count"] = vertex_count
                    meta["face_count"] = face_count
                    meta["execution_device"] = device
                    meta["retry_attempts"] = attempt
                    with open(metadata_path, "w") as f:
                        json.dump(meta, f, indent=4)
                except Exception as js_err:
                    logger.error(f"Failed to append mesh properties in result metadata: {js_err}")

            end_time = time.time()
            duration = end_time - start_time
            
            # Log structured execution details to logs/pipeline.log
            logger.info(
                f"\nStage: Hunyuan3D-2 Shape Generation\n"
                f"Status: Success\n"
                f"Attempt: {attempt + 1}\n"
                f"Device: {device.upper()}\n"
                f"Time: {duration:.2f} Seconds\n"
                f"Vertices: {vertex_count}\n"
                f"Faces: {face_count}\n"
                f"Output Mesh: {glb_dest_path}\n"
            )
            
            cleanup_memory()
            return {
                "success": True,
                "duration_sec": duration,
                "vertex_count": vertex_count,
                "face_count": face_count,
                "mesh_path": glb_dest_path,
                "device": device
            }
            
        except (torch.cuda.OutOfMemoryError, RuntimeError, Exception) as e:
            is_oom = isinstance(e, torch.cuda.OutOfMemoryError) or "out of memory" in str(e).lower() or "CUDA out of memory" in str(e)
            logger.error(f"Shape Gen Attempt {attempt + 1} failed on {device.upper()}: {e}")
            
            if pipeline is not None:
                try:
                    unload_hunyuan3d_model(pipeline)
                except Exception:
                    pass
                pipeline = None
            
            cleanup_memory()
            last_error = e
            
            if is_oom:
                logger.warning(f"CUDA Out Of Memory encountered. Progressing retry strategy.")
            else:
                logger.warning(f"Standard error encountered. Progressing retry strategy.")
                
    # If all attempts fail
    end_time = time.time()
    duration = end_time - start_time
    logger.error(
        f"\nStage: Hunyuan3D-2 Shape Generation\n"
        f"Status: Failed All Attempts\n"
        f"Time: {duration:.2f} Seconds\n"
        f"Error: {str(last_error)}\n"
    )
    raise last_error

def run_texture_generation_pipeline(job_id: str, rgba_path: str) -> dict:
    """Executes Stage 6 of the pipeline: Hunyuan3D-2 Texture Generation (Phase 15).
    
    Loads the untextured mesh, synthesizes PBR textures from the RGBA input,
    applies the texture maps, saves to outputs/meshes/<job_id>_model.glb, and unloads model.
    Implements a progressive retry strategy with automatic CPU fallback.
    """
    start_time = time.time()
    logger.info(f"Starting Hunyuan3D-2 Texture Generation for Job ID: {job_id}")
    
    # Resolve job directory paths
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    glb_src_path = os.path.join(job_dir, "model.glb")
    
    # Target destinations
    meshes_dir = os.path.join(settings.OUTPUT_DIR, "meshes")
    os.makedirs(meshes_dir, exist_ok=True)
    final_glb_path = os.path.join(meshes_dir, f"{job_id}_model.glb")
    
    # Ensure source mesh exists
    if not os.path.exists(glb_src_path):
        raise FileNotFoundError(f"Source untextured mesh model.glb not found at {glb_src_path}")
        
    # Progressive retry configurations:
    # 1. Normal GPU: low-memory setting (resolution 256)
    # 2. Lower-Res GPU: lowest resolution (resolution 128)
    # 3. CPU Fallback: lowest resolution on CPU (resolution 128)
    tries = [
        {"device": "cuda", "resolution": settings.hunyuan3d.texture_resolution},
        {"device": "cuda", "resolution": 128},
        {"device": "cpu", "resolution": 128}
    ]
    
    last_error = None
    for attempt, config in enumerate(tries):
        device = config["device"]
        resolution = config["resolution"]
        
        logger.info(f"Texture Gen Attempt {attempt + 1}/{len(tries)}: device={device.upper()}, resolution={resolution}")
        log_memory_status(f"Before Texture Gen Attempt {attempt + 1}")
        
        pipeline = None
        try:
            # Step 1: Load untextured mesh
            logger.info(f"Loading untextured mesh from: {glb_src_path}")
            mesh = trimesh.load(glb_src_path)
            
            # If it's a Scene, extract the first geometry
            if isinstance(mesh, trimesh.Scene):
                geoms = list(mesh.geometry.values())
                if not geoms:
                    raise ValueError("Source model.glb contains no geometry meshes.")
                mesh = geoms[0]
                
            # Step 2: Load Hunyuan3D-2 texture pipeline
            logger.info("Loading Hunyuan3D-2 texture synthesis model...")
            pipeline, _ = load_hunyuan3d_model(model_type="texture", device=device)
            
            # Step 3: Run texture synthesis
            logger.info(f"Synthesizing texture map with resolution={resolution}")
            textured_mesh = generate_texture(rgba_path, mesh, pipeline, resolution=resolution)
            
            # Step 4: Export self-contained textured GLB to outputs/meshes/
            textured_mesh.export(final_glb_path, file_type="glb")
            logger.info(f"Saved final textured model to: {final_glb_path}")
            
            # Overwrite/save to outputs/<job_id>/model.glb as well for completeness
            outputs_model_path = os.path.join(job_dir, "model.glb")
            textured_mesh.export(outputs_model_path, file_type="glb")
            logger.info(f"Overwrote untextured model in job directory: {outputs_model_path}")
            
            # Step 5: Unload model to recover VRAM immediately
            logger.info("Unloading Hunyuan3D-2 texture synthesis model...")
            unload_hunyuan3d_model(pipeline)
            pipeline = None
            
            # Step 6: Update result.json via artifacts_manager
            artifacts_manager.add_file_artifact(job_id, "model", outputs_model_path, "model.glb")
            artifacts_manager.add_completed_phase(job_id, "texture_generation")
            
            # Update metadata JSON file
            metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r") as f:
                        meta = json.load(f)
                    meta["stage"] = "Hunyuan3D-2 Texture Generation"
                    meta["textured_mesh_path"] = final_glb_path
                    meta["texture_resolution"] = resolution
                    meta["texture_device"] = device
                    meta["texture_retry_attempts"] = attempt
                    with open(metadata_path, "w") as f:
                        json.dump(meta, f, indent=4)
                except Exception as js_err:
                    logger.error(f"Failed to append texture properties in result metadata: {js_err}")

            end_time = time.time()
            duration = end_time - start_time
            
            # Log structured execution details to logs/pipeline.log
            logger.info(
                f"\nStage: Hunyuan3D-2 Texture Generation\n"
                f"Status: Success\n"
                f"Attempt: {attempt + 1}\n"
                f"Device: {device.upper()}\n"
                f"Time: {duration:.2f} Seconds\n"
                f"Texture Resolution: {resolution}\n"
                f"Output Textured GLB: {final_glb_path}\n"
            )
            
            cleanup_memory()
            return {
                "success": True,
                "duration_sec": duration,
                "textured_mesh_path": final_glb_path,
                "device": device
            }
            
        except (torch.cuda.OutOfMemoryError, RuntimeError, Exception) as e:
            is_oom = isinstance(e, torch.cuda.OutOfMemoryError) or "out of memory" in str(e).lower() or "CUDA out of memory" in str(e)
            logger.error(f"Texture Gen Attempt {attempt + 1} failed on {device.upper()}: {e}")
            
            if pipeline is not None:
                try:
                    unload_hunyuan3d_model(pipeline)
                except Exception:
                    pass
                pipeline = None
            
            cleanup_memory()
            last_error = e
            
            if is_oom:
                logger.warning(f"CUDA Out Of Memory encountered. Progressing retry strategy.")
            else:
                logger.warning(f"Standard error encountered. Progressing retry strategy.")
                
    # If all attempts fail
    end_time = time.time()
    duration = end_time - start_time
    logger.error(
        f"\nStage: Hunyuan3D-2 Texture Generation\n"
        f"Status: Failed All Attempts\n"
        f"Time: {duration:.2f} Seconds\n"
        f"Error: {str(last_error)}\n"
    )
    raise last_error

def run_mesh_validation_pipeline(job_id: str) -> dict:
    """Executes Stage 7 of the pipeline: Open3D Mesh Validation (Phase 16).
    
    Loads the textured GLB using Open3D, verifies vertices/faces, computes vertex normals,
    consistently orients them, and records mesh statistics.
    """
    start_time = time.time()
    logger.info(f"Starting Open3D Mesh Validation for Job ID: {job_id}")
    
    try:
        from backend.app.services.mesh_service import mesh_service
        stats = mesh_service.validate_job_mesh(job_id)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: Open3D Mesh Validation\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Mesh Stats: {stats}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "stats": stats
        }
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: Open3D Mesh Validation\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

def run_pointcloud_generation_pipeline(job_id: str) -> dict:
    """Executes Stage 8 of the pipeline: Point Cloud Generation (Phase 17).
    
    Loads the validated GLB mesh using Open3D, samples points using Poisson Disk Sampling,
    verifies normals and colors, and saves outputs/pointcloud/<job_id>_pointcloud.ply.
    """
    start_time = time.time()
    logger.info(f"Starting Point Cloud Generation for Job ID: {job_id}")
    
    try:
        from backend.app.services.pointcloud_service import pointcloud_service
        stats = pointcloud_service.generate_job_pointcloud(job_id)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: Point Cloud Generation\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Point Cloud Stats: {stats}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "stats": stats
        }
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: Point Cloud Generation\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

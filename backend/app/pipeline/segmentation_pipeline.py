import os
import time
import json
import numpy as np
from PIL import Image
from backend.app.core.settings import settings
from backend.app.utils.logger import logger
from ai_models.sam2.loader import load_sam2_model, unload_sam2_model
from ai_models.sam2.segment import segment_image
from backend.app.utils.artifacts_manager import artifacts_manager

def run_segmentation_pipeline(job_id: str, image_path: str) -> dict:
    """Executes SAM 2 segmentation (Phase 12).
    
    Loads SAM 2, reads the bounding box from metadata, extracts a pixel-accurate mask,
    generates mask.png, segmentation.png, and mask_overlay.png, and unloads SAM 2.
    """
    start_time = time.time()
    logger.info(f"Starting SAM 2 Segmentation for Job ID: {job_id}")
    
    # Resolve job directory paths
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
    bbox = None
    
    # Step 1: Read the bounding box from metadata
    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r") as f:
                meta = json.load(f)
                bbox = meta.get("bbox")
        except Exception as e:
            logger.error(f"Failed to read bounding box from metadata: {e}")

    # Fallback to default bbox if metadata is empty or missing (e.g. during standalone tests)
    if bbox is None:
        logger.warning("No bounding box found in metadata. Using full image boundaries as fallback.")
        with Image.open(image_path) as test_img:
            w, h = test_img.size
            bbox = [0, 0, w, h]

    model = None
    try:
        # Step 2: Load SAM 2 model
        logger.info("Loading SAM 2 model into memory...")
        model, processor = load_sam2_model()
        
        # Step 3: Execute segmentation
        logger.info(f"Segmenting object with bounding box prompt: {bbox}")
        binary_mask = segment_image(image_path, bbox, model, processor)
        
        # Step 4: Unload model to recover VRAM immediately
        logger.info("Unloading SAM 2 model...")
        unload_sam2_model(model)
        model = None
        
        # Step 5: Save outputs
        # A. mask.png (1-channel grayscale binary mask)
        mask_path = os.path.join(job_dir, "mask.png")
        mask_img = Image.fromarray(binary_mask, mode="L")
        mask_img.save(mask_path)
        
        # B. segmentation.png (Transparent RGBA cut-out of the object)
        seg_path = os.path.join(job_dir, "segmentation.png")
        orig_img = Image.open(image_path).convert("RGB")
        rgba_img = orig_img.copy()
        rgba_img.putalpha(mask_img)
        rgba_img.save(seg_path, "PNG")
        
        # C. mask_overlay.png (Visual verification check with blue mask colored overlay)
        overlay_path = os.path.join(job_dir, "mask_overlay.png")
        orig_np = np.array(orig_img)
        overlay_np = orig_np.copy()
        mask_indices = (binary_mask == 255)
        # Apply semi-transparent blue tint over the object area using numpy type casting
        overlay_np[mask_indices, 0] = (0.2 * orig_np[mask_indices, 0]).astype(np.uint8)
        overlay_np[mask_indices, 1] = (0.2 * orig_np[mask_indices, 1]).astype(np.uint8)
        overlay_np[mask_indices, 2] = (0.8 * 255 + 0.2 * orig_np[mask_indices, 2]).astype(np.uint8)
        overlay_img = Image.fromarray(overlay_np)
        overlay_img.save(overlay_path)
        
        # Step 6: Update result.json via artifacts_manager
        artifacts_manager.add_file_artifact(job_id, "mask", mask_path, "mask.png")
        artifacts_manager.add_file_artifact(job_id, "segmentation", seg_path, "segmentation.png")
        artifacts_manager.add_file_artifact(job_id, "mask_overlay", overlay_path, "mask_overlay.png")
        artifacts_manager.add_completed_phase(job_id, "segmentation")
        
        # Update metadata JSON file
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                meta["stage"] = "SAM2.1 Segmentation"
                meta["mask_path"] = mask_path
                meta["segmentation_path"] = seg_path
                with open(metadata_path, "w") as f:
                    json.dump(meta, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append segmentation in result metadata: {js_err}")

        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: SAM2.1 Segmentation\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Output Mask: {mask_path}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "mask_path": mask_path,
            "segmentation_path": seg_path,
            "mask_overlay_path": overlay_path
        }
        
    except Exception as e:
        if model is not None:
            unload_sam2_model(model)
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: SAM2.1 Segmentation\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

def run_background_removal_pipeline(job_id: str, image_path: str) -> dict:
    """Executes background removal using rembg and SAM 2 mask (Phase 13).
    
    Generates a clean transparent RGBA image outputs/<job_id>/rgba.png.
    """
    start_time = time.time()
    logger.info(f"Starting Background Removal for Job ID: {job_id}")
    
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    mask_path = os.path.join(job_dir, "mask.png")
    
    # Fallback if mask is missing (e.g. in test setup)
    if not os.path.exists(mask_path):
        logger.warning("SAM 2 mask not found. Creating a temporary solid mask.")
        with Image.open(image_path) as img:
            temp_mask = Image.new("L", img.size, color=255)
            os.makedirs(job_dir, exist_ok=True)
            temp_mask.save(mask_path)
            
    rgba_dest_path = os.path.join(job_dir, "rgba.png")
    
    try:
        from ai_models.rembg.remove import remove_background
        
        final_rgba = remove_background(image_path, mask_path)
        final_rgba.save(rgba_dest_path, "PNG")
        logger.info(f"Saved background removed RGBA image to: {rgba_dest_path}")
        
        # Update result.json and completed phases
        artifacts_manager.add_file_artifact(job_id, "rgba", rgba_dest_path, "rgba.png")
        artifacts_manager.add_completed_phase(job_id, "background_removal")
        
        # Update metadata JSON file
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                meta["stage"] = "Background Removal"
                meta["rgba_path"] = rgba_dest_path
                with open(metadata_path, "w") as f:
                    json.dump(meta, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append background removal in result metadata: {js_err}")
                
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(
            f"\nStage: Background Removal\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Output RGBA: {rgba_dest_path}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "rgba_path": rgba_dest_path
        }
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: Background Removal\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e


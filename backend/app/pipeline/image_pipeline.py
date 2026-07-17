import os
import time
from backend.app.core.settings import settings
from backend.app.utils.logger import logger
from backend.app.utils.image_utils import apply_clahe_to_image
from backend.app.services.image_service import image_service
from backend.app.utils.artifacts_manager import artifacts_manager

def run_image_pipeline(job_id: str, original_image_path: str) -> dict:
    """Executes the image analysis and conditional CLAHE enhancement pipeline stage.
    
    Generates enhanced image under data/temp/<job_id>_enhanced.png if needed,
    and returns pipeline metrics dictionary.
    """
    start_time = time.time()
    logger.info(f"Starting Image Processing stage for Job ID: {job_id}")
    
    try:
        # Step 1: Run image properties analysis and output result JSON (Phase 7)
        analysis_metadata = image_service.analyze_job_image(job_id, original_image_path)
        clahe_required = analysis_metadata.get("clahe_required", False)
        
        # Save analysis stage completion
        artifacts_manager.add_completed_phase(job_id, "analysis")
        
        enhanced_image_path = None
        
        # Step 2: Apply CLAHE if analysis flags it (Phase 8)
        # Apply low-memory downscaling resize if configured
        limits = settings.image_processing.image
        if getattr(limits, "low_memory_resize", False):
            from PIL import Image
            try:
                with Image.open(original_image_path) as img:
                    w, h = img.size
                    target_sz = getattr(limits, "target_size", 1024)
                    if w > target_sz or h > target_sz:
                        logger.info(f"Low memory downscaling resize enabled. Resizing from {w}x{h} to target max {target_sz}px.")
                        img.thumbnail((target_sz, target_sz), Image.Resampling.LANCZOS)
                        img.save(original_image_path)
            except Exception as resize_err:
                logger.warning(f"Failed to apply low memory image resize downscaling: {resize_err}")

        if clahe_required:
            logger.info("Image flagged as dark/low-contrast. Applying CLAHE enhancement.")
            os.makedirs(settings.TEMP_DIR, exist_ok=True)
            
            # Extract file format from original image path
            ext = original_image_path.split(".")[-1].lower() if "." in original_image_path else "png"
            enhanced_image_path = os.path.join(settings.TEMP_DIR, f"{job_id}_enhanced.{ext}")
            
            # Load CLAHE config
            clahe_config = settings.image_processing.clahe
            
            apply_clahe_to_image(
                file_path=original_image_path,
                dest_path=enhanced_image_path,
                clip_limit=clahe_config.clip_limit,
                tile_grid_size=clahe_config.tile_grid_size
            )
            
            # Add enhanced image artifact to outputs/<job_id>/
            artifacts_manager.add_file_artifact(job_id, "enhanced", enhanced_image_path, "enhanced.png")
        else:
            logger.info("Image brightness and contrast within standard thresholds. Bypassing CLAHE.")
            
        # Save clahe stage completion
        artifacts_manager.add_completed_phase(job_id, "clahe")
            
        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: Image Processing\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"CLAHE Applied: {clahe_required}\n"
            f"Output File: {enhanced_image_path or original_image_path}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "clahe_applied": clahe_required,
            "enhanced_image_path": enhanced_image_path
        }
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: Image Processing\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

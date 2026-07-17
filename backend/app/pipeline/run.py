import os
from backend.app.core.settings import settings
from backend.app.utils.logger import logger
from backend.app.utils.artifacts_manager import artifacts_manager

# Import all individual pipeline stages
from backend.app.pipeline.image_pipeline import run_image_pipeline
from backend.app.pipeline.detection_pipeline import (
    run_detection_pipeline_stage1,
    run_detection_pipeline_stage2,
    run_detection_pipeline_stage3,
)
from backend.app.pipeline.segmentation_pipeline import (
    run_segmentation_pipeline,
    run_background_removal_pipeline,
)
from backend.app.pipeline.generation_pipeline import (
    run_shape_generation_pipeline,
    run_texture_generation_pipeline,
    run_mesh_validation_pipeline,
    run_pointcloud_generation_pipeline,
)
from backend.app.pipeline.pointcloud_pipeline import run_dbscan_segmentation_pipeline

def execute_full_reconstruction_pipeline(job_id: str, original_image_path: str):
    """Executes all 14 pipeline stages sequentially in the background for a job."""
    logger.info(f"Starting Background Reconstruction Pipeline for Job: {job_id}")
    try:
        # 1. Image Analysis & CLAHE Enhancement (completed_phases: analysis, clahe)
        res = run_image_pipeline(job_id, original_image_path)
        # Use enhanced image if available, else original
        working_img = res.get("enhanced_image_path") or original_image_path
        if not working_img:
            working_img = original_image_path

        # 2. VLM Captioning (completed_phases: caption_generation)
        res_stage1 = run_detection_pipeline_stage1(job_id, working_img)
        prompt = res_stage1["detection_prompt"]

        # 3. GroundingDINO Detection (completed_phases: groundingdino_detection)
        run_detection_pipeline_stage2(job_id, working_img, prompt)

        # 4. Florence-2 Part Detection (completed_phases: part_detection)
        run_detection_pipeline_stage3(job_id, working_img)

        # 5. SAM2.1 Segmentation (completed_phases: segmentation)
        run_segmentation_pipeline(job_id, working_img)

        # 6. Background Removal (completed_phases: background_removal)
        run_background_removal_pipeline(job_id, working_img)
        rgba_path = os.path.join(settings.OUTPUT_DIR, job_id, "rgba.png")

        # 7. Hunyuan3D-2 Shape Generation (completed_phases: shape_generation)
        run_shape_generation_pipeline(job_id, rgba_path)

        # 8. Hunyuan3D-2 Texture Generation (completed_phases: texture_generation)
        run_texture_generation_pipeline(job_id, rgba_path)

        # 9. Mesh Validation (completed_phases: mesh_validation)
        run_mesh_validation_pipeline(job_id)

        # 10. Point Cloud Generation (completed_phases: pointcloud_generation)
        run_pointcloud_generation_pipeline(job_id)

        # 11. DBSCAN Segmentation (completed_phases: dbscan_segmentation)
        run_dbscan_segmentation_pipeline(job_id)

        # Update final status to completed
        artifacts_manager.update_status(job_id, "completed")
        logger.info(f"Background Reconstruction Pipeline completed successfully for Job: {job_id}")

    except Exception as e:
        logger.error(f"Background Reconstruction Pipeline failed for Job {job_id}: {e}", exc_info=True)
        artifacts_manager.update_status(job_id, "failed")

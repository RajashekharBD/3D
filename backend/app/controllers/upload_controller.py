import os
from fastapi import UploadFile, BackgroundTasks
from backend.app.services.storage_service import storage_service
from backend.app.services.image_service import image_service
from backend.app.schemas.upload_schema import UploadResponse
from backend.app.utils.artifacts_manager import artifacts_manager
from backend.app.pipeline.run import execute_full_reconstruction_pipeline
from backend.app.core.settings import settings

class UploadController:
    def handle_upload(self, file: UploadFile, background_tasks: BackgroundTasks) -> UploadResponse:
        """Handles upload saving, executes Phase 6 validation, and returns job ID."""
        job_id = storage_service.generate_job_id()
        saved_path = storage_service.save_upload(file, job_id)
        
        try:
            # Phase 6: Programmatic image validation
            image_service.validate_job_image(saved_path)
        except Exception:
            # Clean up immediately if validation fails to prevent leaked files
            if os.path.exists(saved_path):
                os.remove(saved_path)
            raise
            
        # Initialise job structure and save original.png
        artifacts_manager.init_job(job_id, saved_path)
        # Mark validation phase as complete
        artifacts_manager.add_completed_phase(job_id, "validation")
        
        # Add background task to run the complete reconstruction pipeline
        original_png_path = os.path.join(settings.OUTPUT_DIR, job_id, "original.png")
        
        background_tasks.add_task(execute_full_reconstruction_pipeline, job_id, original_png_path)
        
        return UploadResponse(job_id=job_id)

upload_controller = UploadController()

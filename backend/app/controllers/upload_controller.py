from fastapi import UploadFile
from backend.app.services.storage_service import storage_service
from backend.app.schemas.upload_schema import UploadResponse

class UploadController:
    def handle_upload(self, file: UploadFile) -> UploadResponse:
        """Handles validation and file saving, returning a unique job ID."""
        job_id = storage_service.generate_job_id()
        storage_service.save_upload(file, job_id)
        return UploadResponse(job_id=job_id)

upload_controller = UploadController()

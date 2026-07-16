import os
import uuid
import shutil
from fastapi import UploadFile
from backend.app.core.settings import settings
from backend.app.core.exceptions import BaseAppException

class StorageService:
    def __init__(self):
        self.input_dir = "data/input"
        self.temp_dir = settings.TEMP_DIR
        self.output_dir = settings.OUTPUT_DIR
        
        # Ensure directories exist
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "meshes"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "pointcloud"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "metadata"), exist_ok=True)

    def generate_job_id(self) -> str:
        """Generate a unique job ID."""
        return str(uuid.uuid4())

    def validate_file(self, file: UploadFile) -> None:
        """Validate file size and extension based on configuration."""
        # 1. Validate Extension
        filename = file.filename or ""
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        if ext not in settings.app.allowed_extensions:
            raise BaseAppException(
                status_code=400,
                message=f"Unsupported file extension '.{ext}'. Allowed: {', '.join(settings.app.allowed_extensions)}",
                stage="Validation"
            )

        # 2. Validate Size
        # Seek to end to get size
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0) # Reset pointer
        
        max_size_bytes = settings.app.max_upload_size_mb * 1024 * 1024
        if size > max_size_bytes:
            raise BaseAppException(
                status_code=400,
                message=f"File size ({size / (1024*1024):.2f} MB) exceeds maximum allowed size of {settings.app.max_upload_size_mb} MB.",
                stage="Validation"
            )

    def save_upload(self, file: UploadFile, job_id: str) -> str:
        """Save the uploaded file and return the saved path."""
        self.validate_file(file)
        
        filename = file.filename or "uploaded_image"
        ext = filename.split(".")[-1].lower() if "." in filename else "png"
        
        dest_filename = f"{job_id}_original.{ext}"
        dest_path = os.path.join(self.input_dir, dest_filename)
        
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return dest_path

storage_service = StorageService()

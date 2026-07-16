from fastapi import APIRouter, UploadFile, File
from backend.app.controllers.upload_controller import upload_controller
from backend.app.schemas.upload_schema import UploadResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
def upload_image(image: UploadFile = File(...)):
    """Uploads an image, validates it, and generates a new reconstruction job."""
    return upload_controller.handle_upload(image)

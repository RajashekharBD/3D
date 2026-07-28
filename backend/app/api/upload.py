from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends
from backend.app.controllers.upload_controller import upload_controller
from backend.app.schemas.upload_schema import UploadResponse
from backend.app.core.auth import get_current_user

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
def upload_image(
    background_tasks: BackgroundTasks, 
    image: UploadFile = File(...), 
    current_user: dict = Depends(get_current_user)
):
    """Uploads an image, validates it, and generates a new reconstruction job."""
    return upload_controller.handle_upload(image, background_tasks, current_user)


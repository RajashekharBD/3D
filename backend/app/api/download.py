from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from backend.app.controllers.download_controller import download_controller
from backend.app.core.auth import get_current_user

router = APIRouter()


@router.get("/download/{job_id}/{artifact_key}", response_class=FileResponse)
def download_artifact(job_id: str, artifact_key: str, current_user: dict = Depends(get_current_user)):
    """Downloads a specific artifact for the given job as an attachment."""
    return download_controller.get_artifact(job_id, artifact_key, current_user)



@router.get("/download/{job_id}")
def list_artifacts(job_id: str, current_user: dict = Depends(get_current_user)):
    """Lists available artifacts for the given job and their availability status."""
    return download_controller.list_available_artifacts(job_id, current_user)

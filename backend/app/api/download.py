from fastapi import APIRouter
from fastapi.responses import FileResponse
from backend.app.controllers.download_controller import download_controller

router = APIRouter()


@router.get("/download/{job_id}/{artifact_key}", response_class=FileResponse)
def download_artifact(job_id: str, artifact_key: str):
    """Downloads a specific artifact for the given job as an attachment."""
    return download_controller.get_artifact(job_id, artifact_key)


@router.get("/download/{job_id}")
def list_artifacts(job_id: str):
    """Lists available artifacts for the given job and their availability status."""
    return download_controller.list_available_artifacts(job_id)

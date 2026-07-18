from fastapi import APIRouter, Depends
from backend.app.controllers.pipeline_controller import pipeline_controller
from backend.app.schemas.pipeline_schema import PipelineStatusResponse
from backend.app.core.auth import get_current_user

router = APIRouter()


@router.get("/pipeline/status/{job_id}", response_model=PipelineStatusResponse)
def get_pipeline_status(job_id: str, current_user: dict = Depends(get_current_user)):
    """Returns the current pipeline processing status and progress for a job."""
    return pipeline_controller.get_status(job_id, current_user)

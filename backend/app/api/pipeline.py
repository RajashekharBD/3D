from fastapi import APIRouter
from backend.app.controllers.pipeline_controller import pipeline_controller
from backend.app.schemas.pipeline_schema import PipelineStatusResponse

router = APIRouter()


@router.get("/pipeline/status/{job_id}", response_model=PipelineStatusResponse)
def get_pipeline_status(job_id: str):
    """Returns the current pipeline processing status and progress for a job."""
    return pipeline_controller.get_status(job_id)

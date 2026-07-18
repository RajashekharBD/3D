from fastapi import APIRouter, Depends, Query
from backend.app.core.auth import get_current_user
from backend.app.controllers.history_controller import history_controller

router = APIRouter()

@router.get("/history")
def get_history(
    filename: str = Query(None, description="Filter by original filename"),
    status: str = Query(None, description="Filter by processing status"),
    sort_by: str = Query("newest", description="Sorting order: newest or oldest"),
    page: int = Query(1, ge=1, description="Page number"),
    current_user: dict = Depends(get_current_user)
):
    """Retrieves paginated processing history for the authenticated user."""
    return history_controller.get_history(current_user, filename, status, sort_by, page)

@router.get("/history/{job_id}")
def get_job_detail(job_id: str, current_user: dict = Depends(get_current_user)):
    """Retrieves full details and associated artifacts of a specific job."""
    return history_controller.get_job_detail(job_id, current_user)

@router.delete("/history/{job_id}")
def delete_job(job_id: str, current_user: dict = Depends(get_current_user)):
    """Performs soft delete of a job and cleans up its local files."""
    return history_controller.delete_job(job_id, current_user)

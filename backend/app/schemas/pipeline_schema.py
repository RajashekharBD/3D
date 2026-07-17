from pydantic import BaseModel
from typing import List, Optional, Dict


class PipelineStatusResponse(BaseModel):
    """Response schema for the pipeline status endpoint."""
    job_id: str
    status: str  # "running", "completed", "failed"
    current_stage: str
    progress: int  # 0–100
    completed_phases: List[str]
    artifacts: Dict[str, str]
    message: Optional[str] = None

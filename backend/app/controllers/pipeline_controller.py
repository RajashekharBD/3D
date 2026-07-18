import os
from fastapi import HTTPException
from backend.app.core.settings import settings
from backend.app.utils.artifacts_manager import artifacts_manager
from backend.app.schemas.pipeline_schema import PipelineStatusResponse
from backend.app.core.database import db

# Ordered list of pipeline phases with human-readable labels and cumulative progress.
# Progress values represent the percentage when that phase completes.
PIPELINE_PHASES = [
    {"key": "upload",                  "label": "Upload",                       "progress": 5},
    {"key": "validation",              "label": "Image Validation",             "progress": 8},
    {"key": "analysis",                "label": "Image Analysis",               "progress": 12},
    {"key": "clahe",                   "label": "CLAHE Enhancement",            "progress": 16},
    {"key": "caption_generation",      "label": "Florence-2 Captioning",        "progress": 22},
    {"key": "groundingdino_detection", "label": "GroundingDINO Detection",      "progress": 30},
    {"key": "part_detection",          "label": "Florence-2 Part Detection",    "progress": 36},
    {"key": "segmentation",            "label": "SAM2.1 Segmentation",          "progress": 44},
    {"key": "background_removal",      "label": "Background Removal",           "progress": 50},
    {"key": "shape_generation",        "label": "Hunyuan3D-2 Shape Generation", "progress": 65},
    {"key": "texture_generation",      "label": "Hunyuan3D-2 Texture Generation", "progress": 78},
    {"key": "mesh_validation",         "label": "Mesh Validation",              "progress": 82},
    {"key": "pointcloud_generation",   "label": "Point Cloud Generation",       "progress": 90},
    {"key": "dbscan_segmentation",     "label": "DBSCAN Segmentation",          "progress": 98},
]


class PipelineController:
    """Controller that computes pipeline progress from result.json."""

    def get_status(self, job_id: str, current_user: dict) -> PipelineStatusResponse:
        """Reads result.json and computes current stage + progress percentage after checking ownership."""
        if db.is_enabled:
            try:
                res = db.get_client().table("jobs").select("user_id").eq("job_id", job_id).execute()
                if not res.data:
                    raise HTTPException(status_code=404, detail="Job not found.")
                if res.data[0]["user_id"] != current_user["id"]:
                    raise HTTPException(status_code=403, detail="Forbidden: You do not own this job.")
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise
                raise HTTPException(status_code=500, detail=f"Database ownership verification failed: {e}")

        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)

        # Check if job directory exists
        if not os.path.isdir(job_dir):
            return PipelineStatusResponse(
                job_id=job_id,
                status="not_found",
                current_stage="Unknown",
                progress=0,
                completed_phases=[],
                artifacts={},
                message=f"Job '{job_id}' does not exist."
            )

        data = artifacts_manager._read_result_json(job_id)
        completed = data.get("completed_phases", [])
        job_status = data.get("status", "running")
        artifacts = data.get("artifacts", {})

        # Compute progress and determine current stage
        progress = 0
        current_stage = "Initializing Pipeline"

        if job_status == "completed":
            progress = 100
            current_stage = "Completed"
        elif job_status == "failed":
            # Find the last completed phase for context
            current_stage = "Failed"
            for phase in PIPELINE_PHASES:
                if phase["key"] in completed:
                    progress = phase["progress"]
        else:
            # Walk phases in order; last completed phase determines progress
            last_completed_idx = -1
            for idx, phase in enumerate(PIPELINE_PHASES):
                if phase["key"] in completed:
                    last_completed_idx = idx
                    progress = phase["progress"]

            # Current stage is the next uncompleted phase
            next_idx = last_completed_idx + 1
            if next_idx < len(PIPELINE_PHASES):
                current_stage = PIPELINE_PHASES[next_idx]["label"]
            else:
                # All phases completed but status not yet set to "completed"
                current_stage = "Finalizing"
                progress = 100

        return PipelineStatusResponse(
            job_id=job_id,
            status=job_status,
            current_stage=current_stage,
            progress=progress,
            completed_phases=completed,
            artifacts=artifacts
        )


pipeline_controller = PipelineController()

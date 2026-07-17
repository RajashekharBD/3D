import os
from fastapi.responses import FileResponse
from fastapi import HTTPException, status
from backend.app.core.settings import settings
from backend.app.utils.logger import logger

# Map of artifact keys to their file paths relative to the outputs directory.
# Paths can contain {job_id} as a placeholder.
ARTIFACT_MAP = {
    "model":                  "meshes/{job_id}_model.glb",
    "pointcloud":             "pointcloud/{job_id}_pointcloud.ply",
    "segmented_pointcloud":   "pointcloud/{job_id}_segmented_pointcloud.ply",
    "rgba":                   "{job_id}/rgba.png",
    "detection":              "{job_id}/detection.png",
    "segmentation":           "{job_id}/segmentation.png",
    "mask_overlay":           "{job_id}/mask_overlay.png",
    "result":                 "{job_id}/result.json",
    "original":               "{job_id}/original.png",
    "enhanced":               "{job_id}/enhanced.png",
    "caption":                "{job_id}/caption.txt",
    "grounding_prompt":       "{job_id}/grounding_prompt.txt",
    "part_detection":         "{job_id}/part_detection.png",
    "mask":                   "{job_id}/mask.png",
}

# MIME types for each artifact
MEDIA_TYPES = {
    ".glb":  "model/gltf-binary",
    ".ply":  "application/octet-stream",
    ".png":  "image/png",
    ".json": "application/json",
    ".txt":  "text/plain",
}


class DownloadController:
    """Controller that resolves artifact paths and returns FileResponse objects."""

    def get_artifact(self, job_id: str, artifact_key: str) -> FileResponse:
        """Returns a downloadable FileResponse for the requested artifact."""
        if artifact_key not in ARTIFACT_MAP:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown artifact key: '{artifact_key}'. "
                       f"Valid keys: {', '.join(sorted(ARTIFACT_MAP.keys()))}"
            )

        relative_path = ARTIFACT_MAP[artifact_key].format(job_id=job_id)
        absolute_path = os.path.join(settings.OUTPUT_DIR, relative_path)

        if not os.path.isfile(absolute_path):
            logger.warning(f"Artifact not found: {absolute_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artifact '{artifact_key}' not found for job '{job_id}'."
            )

        # Determine MIME type from extension
        ext = os.path.splitext(absolute_path)[1].lower()
        media_type = MEDIA_TYPES.get(ext, "application/octet-stream")

        # Build a download filename
        filename = os.path.basename(absolute_path)

        logger.info(f"Serving artifact '{artifact_key}' for job {job_id}: {absolute_path}")
        return FileResponse(
            path=absolute_path,
            media_type=media_type,
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename=\"{filename}\""}
        )

    def list_available_artifacts(self, job_id: str) -> dict:
        """Returns a dict of artifact_key -> bool availability."""
        result = {}
        for key, rel_path in ARTIFACT_MAP.items():
            absolute_path = os.path.join(
                settings.OUTPUT_DIR, rel_path.format(job_id=job_id)
            )
            result[key] = os.path.isfile(absolute_path)
        return {"job_id": job_id, "artifacts": result}


download_controller = DownloadController()

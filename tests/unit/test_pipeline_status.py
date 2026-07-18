import os
import json
import tempfile
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def _create_job_with_phases(job_id: str, phases: list, status: str = "running", output_dir: str = "outputs"):
    """Helper to create a fake job directory with result.json."""
    job_dir = os.path.join(output_dir, job_id)
    os.makedirs(job_dir, exist_ok=True)
    data = {
        "job_id": job_id,
        "status": status,
        "completed_phases": phases,
        "artifacts": {}
    }
    with open(os.path.join(job_dir, "result.json"), "w") as f:
        json.dump(data, f)
    return job_dir


def test_status_not_found():
    """Status endpoint returns not_found for nonexistent job."""
    response = client.get("/api/v1/pipeline/status/nonexistent_job_xyz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "not_found"
    assert data["progress"] == 0
    assert data["message"] is not None


def test_status_running_partial():
    """Status endpoint returns correct progress for a partially completed job."""
    job_id = "test_status_partial_001"
    job_dir = None
    try:
        job_dir = _create_job_with_phases(
            job_id,
            ["upload", "validation", "analysis", "clahe", "caption_generation"],
            status="running"
        )
        response = client.get(f"/api/v1/pipeline/status/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert data["progress"] == 22  # caption_generation is at 22%
        assert data["current_stage"] == "GroundingDINO Detection"
        assert "caption_generation" in data["completed_phases"]
    finally:
        if job_dir and os.path.isdir(job_dir):
            import shutil
            shutil.rmtree(job_dir)


def test_status_completed():
    """Status endpoint returns 100% for a completed job."""
    job_id = "test_status_complete_002"
    job_dir = None
    try:
        job_dir = _create_job_with_phases(
            job_id,
            ["upload", "validation", "analysis", "clahe", "caption_generation",
             "groundingdino_detection", "part_detection", "segmentation",
             "background_removal", "shape_generation", "texture_generation",
             "mesh_validation", "pointcloud_generation", "dbscan_segmentation"],
            status="completed"
        )
        response = client.get(f"/api/v1/pipeline/status/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["progress"] == 100
        assert data["current_stage"] == "Completed"
    finally:
        if job_dir and os.path.isdir(job_dir):
            import shutil
            shutil.rmtree(job_dir)


def test_status_failed():
    """Status endpoint returns failed status with partial progress."""
    job_id = "test_status_failed_003"
    job_dir = None
    try:
        job_dir = _create_job_with_phases(
            job_id,
            ["upload", "validation", "analysis"],
            status="failed"
        )
        response = client.get(f"/api/v1/pipeline/status/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "failed"
        assert data["progress"] == 12  # analysis is at 12%
        assert data["current_stage"] == "Failed"
    finally:
        if job_dir and os.path.isdir(job_dir):
            import shutil
            shutil.rmtree(job_dir)


def test_status_initial_upload_only():
    """Status endpoint returns early progress for a job with only upload phase."""
    job_id = "test_status_upload_004"
    job_dir = None
    try:
        job_dir = _create_job_with_phases(
            job_id,
            ["upload"],
            status="running"
        )
        response = client.get(f"/api/v1/pipeline/status/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert data["progress"] == 5  # upload is at 5%
        assert data["current_stage"] == "Image Validation"
    finally:
        if job_dir and os.path.isdir(job_dir):
            import shutil
            shutil.rmtree(job_dir)

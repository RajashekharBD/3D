import os
import json
import shutil
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def _setup_job_with_artifacts(job_id: str):
    """Creates a job directory with sample artifact files for download testing."""
    job_dir = os.path.join("outputs", job_id)
    meshes_dir = os.path.join("outputs", "meshes")
    pointcloud_dir = os.path.join("outputs", "pointcloud")
    
    os.makedirs(job_dir, exist_ok=True)
    os.makedirs(meshes_dir, exist_ok=True)
    os.makedirs(pointcloud_dir, exist_ok=True)

    # Create sample artifact files
    with open(os.path.join(job_dir, "result.json"), "w") as f:
        json.dump({"job_id": job_id, "status": "completed", "completed_phases": [], "artifacts": {}}, f)

    with open(os.path.join(job_dir, "rgba.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)  # minimal PNG-like stub

    with open(os.path.join(job_dir, "original.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)

    with open(os.path.join(job_dir, "caption.txt"), "w") as f:
        f.write("A sample caption.")

    with open(os.path.join(meshes_dir, f"{job_id}_model.glb"), "wb") as f:
        f.write(b"glTF" + b"\x00" * 100)  # minimal GLB-like stub

    with open(os.path.join(pointcloud_dir, f"{job_id}_pointcloud.ply"), "wb") as f:
        f.write(b"ply\nformat ascii 1.0\nend_header\n")

    return job_dir, meshes_dir, pointcloud_dir


def _teardown_job(job_id: str):
    """Removes all test artifacts."""
    job_dir = os.path.join("outputs", job_id)
    if os.path.isdir(job_dir):
        shutil.rmtree(job_dir)
    # Clean up mesh and pointcloud test files only
    mesh_file = os.path.join("outputs", "meshes", f"{job_id}_model.glb")
    if os.path.isfile(mesh_file):
        os.remove(mesh_file)
    ply_file = os.path.join("outputs", "pointcloud", f"{job_id}_pointcloud.ply")
    if os.path.isfile(ply_file):
        os.remove(ply_file)


def test_download_result_json():
    """Download endpoint serves result.json as attachment."""
    job_id = "test_dl_json_001"
    try:
        _setup_job_with_artifacts(job_id)
        response = client.get(f"/api/v1/download/{job_id}/result")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")
        assert "attachment" in response.headers.get("content-disposition", "")
    finally:
        _teardown_job(job_id)


def test_download_rgba_png():
    """Download endpoint serves rgba.png as image/png."""
    job_id = "test_dl_rgba_002"
    try:
        _setup_job_with_artifacts(job_id)
        response = client.get(f"/api/v1/download/{job_id}/rgba")
        assert response.status_code == 200
        assert "image/png" in response.headers.get("content-type", "")
    finally:
        _teardown_job(job_id)


def test_download_glb_model():
    """Download endpoint serves GLB model file."""
    job_id = "test_dl_glb_003"
    try:
        _setup_job_with_artifacts(job_id)
        response = client.get(f"/api/v1/download/{job_id}/model")
        assert response.status_code == 200
        assert "attachment" in response.headers.get("content-disposition", "")
    finally:
        _teardown_job(job_id)


def test_download_caption_txt():
    """Download endpoint serves caption text file."""
    job_id = "test_dl_caption_004"
    try:
        _setup_job_with_artifacts(job_id)
        response = client.get(f"/api/v1/download/{job_id}/caption")
        assert response.status_code == 200
        assert "text/plain" in response.headers.get("content-type", "")
        assert b"A sample caption." in response.content
    finally:
        _teardown_job(job_id)


def test_download_missing_artifact():
    """Download endpoint returns 404 for a missing artifact file."""
    job_id = "test_dl_missing_005"
    try:
        _setup_job_with_artifacts(job_id)
        # segmentation.png was NOT created in setup
        response = client.get(f"/api/v1/download/{job_id}/segmentation")
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()
    finally:
        _teardown_job(job_id)


def test_download_invalid_artifact_key():
    """Download endpoint returns 400 for an unknown artifact key."""
    job_id = "test_dl_invalid_006"
    try:
        _setup_job_with_artifacts(job_id)
        response = client.get(f"/api/v1/download/{job_id}/nonexistent_key")
        assert response.status_code == 400
        data = response.json()
        assert "Unknown artifact key" in data["detail"]
    finally:
        _teardown_job(job_id)


def test_list_artifacts():
    """List artifacts endpoint returns availability mapping."""
    job_id = "test_dl_list_007"
    try:
        _setup_job_with_artifacts(job_id)
        response = client.get(f"/api/v1/download/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id
        artifacts = data["artifacts"]
        assert artifacts["result"] is True
        assert artifacts["rgba"] is True
        assert artifacts["original"] is True
        assert artifacts["model"] is True
        assert artifacts["caption"] is True
        # These were NOT created
        assert artifacts["segmentation"] is False
        assert artifacts["detection"] is False
    finally:
        _teardown_job(job_id)

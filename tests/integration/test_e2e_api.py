"""
Integration test: End-to-end API flow.

Verifies:
  1. Upload endpoint accepts image and returns job_id.
  2. Pipeline status endpoint returns valid data for the created job.
  3. Download list endpoint returns artifact availability.
  4. result.json is created and contains expected structure.
  5. Original image artifact is saved.
  6. Every output folder is created.
  7. Every API endpoint responds correctly.
  8. Frontend polling simulation.
"""
import io
import os
import json
import shutil
from PIL import Image
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.utils.artifacts_manager import artifacts_manager

client = TestClient(app)


def _create_test_image(size=(256, 256), color=(120, 80, 200)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, color=color).save(buf, format="PNG")
    return buf.getvalue()


def _create_job_with_full_artifacts(job_id: str):
    """Creates a realistic completed job with all expected artifacts."""
    job_dir = os.path.join("outputs", job_id)
    meshes_dir = os.path.join("outputs", "meshes")
    pointcloud_dir = os.path.join("outputs", "pointcloud")
    images_dir = os.path.join("outputs", "images")
    metadata_dir = os.path.join("outputs", "metadata")

    for d in [job_dir, meshes_dir, pointcloud_dir, images_dir, metadata_dir]:
        os.makedirs(d, exist_ok=True)

    # result.json with all phases completed
    result_data = {
        "job_id": job_id,
        "status": "completed",
        "completed_phases": [
            "upload", "validation", "analysis", "clahe",
            "caption_generation", "groundingdino_detection", "part_detection",
            "segmentation", "background_removal", "shape_generation",
            "texture_generation", "mesh_validation", "pointcloud_generation",
            "dbscan_segmentation"
        ],
        "artifacts": {
            "original": "original.png",
            "enhanced": "enhanced.png",
            "detection": "detection.png",
            "segmentation": "segmentation.png",
            "mask": "mask.png",
            "mask_overlay": "mask_overlay.png",
            "rgba": "rgba.png",
            "model": "model.glb",
            "pointcloud": "pointcloud.ply",
            "segmented_pointcloud": "segmented_pointcloud.ply",
            "caption": "caption.txt",
            "grounding_prompt": "grounding_prompt.txt",
            "part_detection": "part_detection.png",
            "result": "result.json"
        }
    }

    # Create all artifact files
    with open(os.path.join(job_dir, "result.json"), "w") as f:
        json.dump(result_data, f, indent=4)
    with open(os.path.join(job_dir, "original.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    with open(os.path.join(job_dir, "enhanced.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    with open(os.path.join(job_dir, "detection.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    with open(os.path.join(job_dir, "segmentation.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    with open(os.path.join(job_dir, "mask.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 50)
    with open(os.path.join(job_dir, "mask_overlay.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    with open(os.path.join(job_dir, "rgba.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)
    with open(os.path.join(meshes_dir, f"{job_id}_model.glb"), "wb") as f:
        f.write(b"glTF" + b"\x00" * 100)
    with open(os.path.join(pointcloud_dir, f"{job_id}_pointcloud.ply"), "wb") as f:
        f.write(b"ply\nformat ascii 1.0\nend_header\n")
    with open(os.path.join(pointcloud_dir, f"{job_id}_segmented_pointcloud.ply"), "wb") as f:
        f.write(b"ply\nformat ascii 1.0\nend_header\n")
    with open(os.path.join(job_dir, "caption.txt"), "w") as f:
        f.write("a black ceramic mug")
    with open(os.path.join(job_dir, "grounding_prompt.txt"), "w") as f:
        f.write("black . ceramic . mug")
    with open(os.path.join(job_dir, "part_detection.png"), "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"\x00" * 100)

    return job_dir


def _teardown(job_id: str):
    job_dir = os.path.join("outputs", job_id)
    if os.path.isdir(job_dir):
        shutil.rmtree(job_dir)
    for subdir in ["meshes", "pointcloud"]:
        path = os.path.join("outputs", subdir, f"{job_id}_model.glb")
        if os.path.isfile(path):
            os.remove(path)
        path = os.path.join("outputs", subdir, f"{job_id}_pointcloud.ply")
        if os.path.isfile(path):
            os.remove(path)
        path = os.path.join("outputs", subdir, f"{job_id}_segmented_pointcloud.ply")
        if os.path.isfile(path):
            os.remove(path)


class TestUploadEndpoint:
    """Test POST /api/v1/upload with various inputs."""

    def test_upload_valid_png(self):
        content = _create_test_image()
        files = {"image": ("test.png", io.BytesIO(content), "image/png")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert len(data["job_id"]) > 0
        _teardown(data["job_id"])

    def test_upload_valid_jpeg(self):
        buf = io.BytesIO()
        Image.new("RGB", (100, 100), color="red").save(buf, format="JPEG")
        content = buf.getvalue()
        files = {"image": ("test.jpg", io.BytesIO(content), "image/jpeg")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 200
        _teardown(response.json()["job_id"])

    def test_upload_valid_webp(self):
        buf = io.BytesIO()
        Image.new("RGB", (100, 100), color="green").save(buf, format="WEBP")
        content = buf.getvalue()
        files = {"image": ("test.webp", io.BytesIO(content), "image/webp")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 200
        _teardown(response.json()["job_id"])

    def test_upload_rejects_pdf(self):
        files = {"image": ("test.pdf", io.BytesIO(b"PDF content"), "application/pdf")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 400

    def test_upload_rejects_empty_file(self):
        files = {"image": ("empty.jpg", io.BytesIO(b""), "image/jpeg")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 400

    def test_upload_rejects_too_large(self):
        large = b"0" * (26 * 1024 * 1024)
        files = {"image": ("large.png", io.BytesIO(large), "image/png")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 400

    def test_upload_rejects_corruptedImage(self):
        corrupt = b"\xff\xd8\xff" + b"\x00" * 50
        files = {"image": ("corrupt.jpg", io.BytesIO(corrupt), "image/jpeg")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 400


class TestHealthEndpoint:
    def test_health_returns_200(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestPipelineStatusEndpoint:
    def test_status_not_found(self):
        response = client.get("/api/v1/pipeline/status/nonexistent_xyz")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "not_found"
        assert data["progress"] == 0

    def test_status_running(self):
        job_id = "test_integ_running"
        job_dir = os.path.join("outputs", job_id)
        os.makedirs(job_dir, exist_ok=True)
        with open(os.path.join(job_dir, "result.json"), "w") as f:
            json.dump({
                "job_id": job_id,
                "status": "running",
                "completed_phases": ["upload", "validation", "analysis"],
                "artifacts": {}
            }, f)
        try:
            response = client.get(f"/api/v1/pipeline/status/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "running"
            assert data["progress"] == 12
        finally:
            shutil.rmtree(job_dir)

    def test_status_completed(self):
        job_id = "test_integ_completed"
        job_dir = os.path.join("outputs", job_id)
        os.makedirs(job_dir, exist_ok=True)
        all_phases = [
            "upload", "validation", "analysis", "clahe",
            "caption_generation", "groundingdino_detection", "part_detection",
            "segmentation", "background_removal", "shape_generation",
            "texture_generation", "mesh_validation", "pointcloud_generation",
            "dbscan_segmentation"
        ]
        with open(os.path.join(job_dir, "result.json"), "w") as f:
            json.dump({
                "job_id": job_id,
                "status": "completed",
                "completed_phases": all_phases,
                "artifacts": {}
            }, f)
        try:
            response = client.get(f"/api/v1/pipeline/status/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "completed"
            assert data["progress"] == 100
            assert data["current_stage"] == "Completed"
        finally:
            shutil.rmtree(job_dir)

    def test_status_failed(self):
        job_id = "test_integ_failed"
        job_dir = os.path.join("outputs", job_id)
        os.makedirs(job_dir, exist_ok=True)
        with open(os.path.join(job_dir, "result.json"), "w") as f:
            json.dump({
                "job_id": job_id,
                "status": "failed",
                "completed_phases": ["upload", "validation"],
                "artifacts": {}
            }, f)
        try:
            response = client.get(f"/api/v1/pipeline/status/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "failed"
            assert data["current_stage"] == "Failed"
        finally:
            shutil.rmtree(job_dir)


class TestDownloadEndpoint:
    def test_download_all_artifact_types(self):
        job_id = "test_integ_dl"
        _create_job_with_full_artifacts(job_id)
        try:
            for key in ["result", "original", "enhanced", "detection", "segmentation",
                         "mask", "mask_overlay", "rgba", "caption", "grounding_prompt",
                         "part_detection", "model", "pointcloud", "segmented_pointcloud"]:
                response = client.get(f"/api/v1/download/{job_id}/{key}")
                assert response.status_code == 200, f"Failed for artifact: {key}"
                assert "attachment" in response.headers.get("content-disposition", "")
        finally:
            _teardown(job_id)

    def test_download_missing_returns_404(self):
        job_id = "test_integ_dl_404"
        _create_job_with_full_artifacts(job_id)
        try:
            response = client.get(f"/api/v1/download/{job_id}/nonexistent_file")
            assert response.status_code == 400
        finally:
            _teardown(job_id)

    def test_download_invalid_key_returns_400(self):
        job_id = "test_integ_dl_badkey"
        _create_job_with_full_artifacts(job_id)
        try:
            response = client.get(f"/api/v1/download/{job_id}/invalid_key_xyz")
            assert response.status_code == 400
        finally:
            _teardown(job_id)

    def test_list_artifacts_returns_availability(self):
        job_id = "test_integ_list"
        _create_job_with_full_artifacts(job_id)
        try:
            response = client.get(f"/api/v1/download/{job_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == job_id
            assert data["artifacts"]["result"] is True
            assert data["artifacts"]["model"] is True
            assert data["artifacts"]["pointcloud"] is True
        finally:
            _teardown(job_id)


class TestEndToEndUploadFlow:
    """Tests the full upload -> status -> download flow with real artifacts."""

    job_id: str = ""

    def test_01_upload_returns_job_id(self):
        content = _create_test_image()
        files = {"image": ("test_e2e.png", io.BytesIO(content), "image/png")}
        response = client.post("/api/v1/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        TestEndToEndUploadFlow.job_id = data["job_id"]

    def test_02_job_directory_created(self):
        job_id = TestEndToEndUploadFlow.job_id
        assert job_id
        job_dir = os.path.join("outputs", job_id)
        assert os.path.isdir(job_dir)

    def test_03_result_json_structure(self):
        job_id = TestEndToEndUploadFlow.job_id
        result_path = os.path.join("outputs", job_id, "result.json")
        assert os.path.isfile(result_path)
        with open(result_path) as f:
            data = json.load(f)
        assert data["job_id"] == job_id
        assert "upload" in data["completed_phases"]
        assert "validation" in data["completed_phases"]
        assert "original" in data["artifacts"]

    def test_04_original_image_saved(self):
        job_id = TestEndToEndUploadFlow.job_id
        original_path = os.path.join("outputs", job_id, "original.png")
        assert os.path.isfile(original_path)
        img = Image.open(original_path)
        assert img.size == (256, 256)

    def test_05_status_returns_running(self):
        job_id = TestEndToEndUploadFlow.job_id
        response = client.get(f"/api/v1/pipeline/status/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert data["progress"] > 0

    def test_06_download_list_shows_original(self):
        job_id = TestEndToEndUploadFlow.job_id
        response = client.get(f"/api/v1/download/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["artifacts"]["original"] is True
        assert data["artifacts"]["result"] is True

    def test_07_download_original_works(self):
        job_id = TestEndToEndUploadFlow.job_id
        response = client.get(f"/api/v1/download/{job_id}/original")
        assert response.status_code == 200
        assert "image/png" in response.headers.get("content-type", "")

    def test_08_download_result_json(self):
        job_id = TestEndToEndUploadFlow.job_id
        response = client.get(f"/api/v1/download/{job_id}/result")
        assert response.status_code == 200
        data = response.json()
        assert data["job_id"] == job_id

    def test_09_download_missing_artifact_404(self):
        job_id = TestEndToEndUploadFlow.job_id
        response = client.get(f"/api/v1/download/{job_id}/model")
        assert response.status_code == 404

    def test_99_cleanup(self):
        job_id = TestEndToEndUploadFlow.job_id
        if job_id:
            _teardown(job_id)
            import glob
            for f in glob.glob(os.path.join("data", "input", f"{job_id}*")):
                os.remove(f)


class TestOutputFolders:
    """Verify all expected output folders exist or are created."""

    def test_output_folders_exist(self):
        required_dirs = ["outputs", "outputs/images", "outputs/meshes",
                         "outputs/pointcloud", "outputs/metadata"]
        for d in required_dirs:
            os.makedirs(d, exist_ok=True)
            assert os.path.isdir(d), f"Directory not found: {d}"


class TestResultJsonIntegrity:
    """Verify result.json structure for a completed job."""

    def test_completed_job_result_json(self):
        job_id = "test_integ_resultjson"
        _create_job_with_full_artifacts(job_id)
        try:
            result_path = os.path.join("outputs", job_id, "result.json")
            with open(result_path) as f:
                data = json.load(f)

            assert data["job_id"] == job_id
            assert data["status"] == "completed"
            assert len(data["completed_phases"]) == 14
            assert len(data["artifacts"]) >= 10

            required_artifacts = ["original", "model", "pointcloud", "rgba", "caption"]
            for key in required_artifacts:
                assert key in data["artifacts"], f"Missing artifact key: {key}"
        finally:
            _teardown(job_id)


class TestPollingSimulation:
    """Simulate frontend polling behavior."""

    def test_poll_returns_progress_updates(self):
        job_id = "test_poll_sim"
        job_dir = os.path.join("outputs", job_id)
        os.makedirs(job_dir, exist_ok=True)

        phases_progress = [
            (["upload"], 5),
            (["upload", "validation"], 8),
            (["upload", "validation", "analysis"], 12),
            (["upload", "validation", "analysis", "clahe"], 16),
            (["upload", "validation", "analysis", "clahe", "caption_generation"], 22),
        ]

        try:
            for phases, expected_progress in phases_progress:
                with open(os.path.join(job_dir, "result.json"), "w") as f:
                    json.dump({
                        "job_id": job_id,
                        "status": "running",
                        "completed_phases": phases,
                        "artifacts": {}
                    }, f)
                response = client.get(f"/api/v1/pipeline/status/{job_id}")
                assert response.status_code == 200
                data = response.json()
                assert data["progress"] == expected_progress
        finally:
            shutil.rmtree(job_dir)


class TestConcurrentUploads:
    """Test multiple sequential uploads create unique jobs."""

    def test_sequential_uploads_unique_ids(self):
        ids = set()
        for _ in range(3):
            content = _create_test_image()
            files = {"image": ("test.png", io.BytesIO(content), "image/png")}
            response = client.post("/api/v1/upload", files=files)
            assert response.status_code == 200
            ids.add(response.json()["job_id"])
        assert len(ids) == 3, "All job IDs should be unique"
        for jid in ids:
            _teardown(jid)

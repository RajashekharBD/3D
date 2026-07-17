import os
import json
import pytest
import shutil
from PIL import Image
from backend.app.pipeline.detection_pipeline import run_detection_pipeline_stage3
from backend.app.core.settings import settings

@pytest.mark.skipif(os.environ.get("SKIP_HF_TESTS") == "true", reason="Skipping HuggingFace model download tests")
def test_florence2_part_detection_success():
    job_id = "test-job-florence-part"
    
    # 1. Create a dummy image
    os.makedirs("data/temp", exist_ok=True)
    image_path = "data/temp/test_part_input.png"
    img = Image.new("RGB", (200, 200), color="blue")
    img.save(image_path)
    
    # Pre-initialize job folder to let artifacts_manager run correctly
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, image_path)

    try:
        # 2. Run stage 3 part detection (querying for "body" and "base")
        result = run_detection_pipeline_stage3(
            job_id=job_id,
            image_path=image_path,
            parts_list=["body", "base"]
        )
        
        assert result["success"] is True
        assert "parts" in result
        
        # Verify result.json has "parts" and is updated
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        result_json_path = os.path.join(job_dir, "result.json")
        part_img_path = os.path.join(job_dir, "part_detection.png")
        
        assert os.path.exists(result_json_path)
        assert os.path.exists(part_img_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "parts" in data
            assert "part_detection" in data["completed_phases"]
            assert data["artifacts"]["part_detection"] == "part_detection.png"
            
    finally:
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

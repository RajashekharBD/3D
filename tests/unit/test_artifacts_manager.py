import os
import json
import pytest
import shutil
from PIL import Image
from backend.app.utils.artifacts_manager import artifacts_manager
from backend.app.core.settings import settings

def test_artifacts_manager_lifecycle():
    job_id = "test-job-artifacts-lifecycle"
    
    # 1. Create a dummy original image
    os.makedirs("data/temp", exist_ok=True)
    temp_img_path = "data/temp/dummy_orig.png"
    img = Image.new("RGB", (100, 100), color="blue")
    img.save(temp_img_path)
    
    try:
        # 2. Init job
        artifacts_manager.init_job(job_id, temp_img_path)
        
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        result_json_path = os.path.join(job_dir, "result.json")
        dest_original_path = os.path.join(job_dir, "original.png")
        
        assert os.path.exists(job_dir)
        assert os.path.exists(result_json_path)
        assert os.path.exists(dest_original_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert data["job_id"] == job_id
            assert data["status"] == "running"
            assert "upload" in data["completed_phases"]
            assert data["artifacts"]["original"] == "original.png"
            
        # 3. Add completed phase
        artifacts_manager.add_completed_phase(job_id, "validation")
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "validation" in data["completed_phases"]
            
        # 4. Add text artifact
        artifacts_manager.add_text_artifact(job_id, "caption", "a blue block", "caption.txt")
        assert os.path.exists(os.path.join(job_dir, "caption.txt"))
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert data["artifacts"]["caption"] == "caption.txt"
            
        # 5. Add file artifact
        temp_enhanced_path = "data/temp/dummy_enhanced.png"
        img_enhanced = Image.new("RGB", (100, 100), color="cyan")
        img_enhanced.save(temp_enhanced_path)
        
        artifacts_manager.add_file_artifact(job_id, "enhanced", temp_enhanced_path, "enhanced.png")
        assert os.path.exists(os.path.join(job_dir, "enhanced.png"))
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert data["artifacts"]["enhanced"] == "enhanced.png"
            
        # Cleanup temp enhanced file
        if os.path.exists(temp_enhanced_path):
            os.remove(temp_enhanced_path)
            
    finally:
        # Cleanup
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)

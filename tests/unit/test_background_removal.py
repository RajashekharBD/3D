import os
import json
import pytest
import shutil
import numpy as np
from PIL import Image, ImageDraw
from backend.app.pipeline.segmentation_pipeline import run_background_removal_pipeline
from backend.app.core.settings import settings

def create_bg_removal_test_image(filename: str) -> str:
    """Creates a simple test image with a colored block in the middle for background removal test."""
    os.makedirs("data/temp", exist_ok=True)
    file_path = os.path.join("data/temp", filename)
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([30, 30, 70, 70], fill=(255, 0, 0)) # Red square
    img.save(file_path)
    return file_path

def test_background_removal_success():
    job_id = "test-job-bg-removal"
    image_path = create_bg_removal_test_image("red_box_bg_rem.png")
    
    # 1. Pre-init job folder
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, image_path)
    
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    mask_path = os.path.join(job_dir, "mask.png")
    
    # Save a binary mask (white box in the middle)
    mask = Image.new("L", (100, 100), color=0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rectangle([30, 30, 70, 70], fill=255)
    mask.save(mask_path)
    
    try:
        # 2. Run the background removal pipeline
        result = run_background_removal_pipeline(job_id, image_path)
        
        assert result["success"] is True
        rgba_path = result["rgba_path"]
        assert os.path.exists(rgba_path)
        
        # 3. Verify output image channels and alpha channel representation
        rgba_img = Image.open(rgba_path)
        assert rgba_img.mode == "RGBA"
        
        rgba_np = np.array(rgba_img)
        # Check channels is 4
        assert rgba_np.shape[2] == 4
        
        # Check that background pixels (outside 30-70 range) have 0 alpha value (transparent)
        assert rgba_np[10, 10, 3] == 0
        
        # Check that foreground pixels (inside 30-70 range) have positive alpha value (opaque)
        # rembg + mask might leave it as 255
        assert rgba_np[50, 50, 3] > 0
        
        # 4. Verify result.json updates
        result_json_path = os.path.join(job_dir, "result.json")
        assert os.path.exists(result_json_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "background_removal" in data["completed_phases"]
            assert data["artifacts"]["rgba"] == "rgba.png"
            
    finally:
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

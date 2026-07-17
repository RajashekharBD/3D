import os
import json
import pytest
import shutil
from PIL import Image, ImageDraw
from backend.app.pipeline.segmentation_pipeline import run_segmentation_pipeline
from backend.app.core.settings import settings

def create_segmentation_test_image(filename: str, color=(255, 0, 0), bg_color=(255, 255, 255)) -> str:
    """Creates a simple test image with a colored block in the middle for segmentation test."""
    os.makedirs("data/temp", exist_ok=True)
    file_path = os.path.join("data/temp", filename)
    
    # 200x200 canvas
    img = Image.new("RGB", (200, 200), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a 50x50 block in the middle
    draw.rectangle([75, 75, 125, 125], fill=color)
    img.save(file_path)
    return file_path

@pytest.mark.skipif(os.environ.get("SKIP_HF_TESTS") == "true", reason="Skipping HuggingFace model download tests")
def test_sam2_segmentation_success():
    job_id = "test-job-sam-segment"
    image_path = create_segmentation_test_image("red_box_seg.png")
    
    # 1. Pre-init job folder and metadata JSON with bounding box coordinates
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, image_path)
    
    metadata_dir = os.path.join(settings.OUTPUT_DIR, "metadata")
    os.makedirs(metadata_dir, exist_ok=True)
    metadata_path = os.path.join(metadata_dir, f"{job_id}_result.json")
    
    # Bounding box coordinates for the middle red square
    bbox_meta = {"bbox": [75, 75, 125, 125]}
    with open(metadata_path, "w") as f:
        json.dump(bbox_meta, f)
        
    try:
        # 2. Run the segmentation pipeline
        result = run_segmentation_pipeline(job_id, image_path)
        
        assert result["success"] is True
        assert os.path.exists(result["mask_path"])
        assert os.path.exists(result["segmentation_path"])
        assert os.path.exists(result["mask_overlay_path"])
        
        # 3. Check result.json updates
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        result_json_path = os.path.join(job_dir, "result.json")
        assert os.path.exists(result_json_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "segmentation" in data["completed_phases"]
            assert data["artifacts"]["mask"] == "mask.png"
            assert data["artifacts"]["segmentation"] == "segmentation.png"
            assert data["artifacts"]["mask_overlay"] == "mask_overlay.png"
            
    finally:
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

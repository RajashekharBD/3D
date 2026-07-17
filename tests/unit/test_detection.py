import os
import json
import pytest
from PIL import Image, ImageDraw
from backend.app.core.settings import settings
from unittest.mock import MagicMock
from backend.app.pipeline.detection_pipeline import run_detection_pipeline_stage2
from backend.app.core.exceptions import NoObjectDetected

def create_detection_test_image(filename: str, color=(255, 0, 0), bg_color=(255, 255, 255)) -> str:
    """Creates an image with a specific solid colored block in the middle for target detection."""
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
def test_groundingdino_detection_success():
    job_id = "test-job-dino-detect"
    image_path = create_detection_test_image("red_box.png", color=(255, 0, 0))
    
    # Run stage 2 detection with prompt "red block"
    # GroundingDINO should locate the red box in the middle
    result = run_detection_pipeline_stage2(job_id, image_path, "red block")
    
    assert result["success"] is True
    assert "bbox" in result
    assert len(result["bbox"]) == 4
    # Bounding box should enclose the middle block (roughly 75, 75, 125, 125)
    xmin, ymin, xmax, ymax = result["bbox"]
    assert xmin < xmax
    assert ymin < ymax
    
    # Check that metadata result exists
    metadata_path = f"outputs/metadata/{job_id}_result.json"
    detection_img_path = f"outputs/images/{job_id}_detection.png"
    assert os.path.exists(metadata_path)
    assert os.path.exists(detection_img_path)
    with open(metadata_path, "r") as f:
        data = json.load(f)
        assert data["bbox"] == result["bbox"]
        assert data["bbox_attempts"] >= 1
        
    # Cleanup
    if os.path.exists(image_path):
        os.remove(image_path)
    if os.path.exists(metadata_path):
        os.remove(metadata_path)
    if os.path.exists(detection_img_path):
        os.remove(detection_img_path)

@pytest.mark.skipif(os.environ.get("SKIP_HF_TESTS") == "true", reason="Skipping HuggingFace model download tests")
def test_groundingdino_no_object_detected():
    job_id = "test-job-dino-fail"
    os.makedirs("data/temp", exist_ok=True)
    image_path = os.path.join("data/temp", "solid_white.png")
    img = Image.new("RGB", (200, 200), color=(255, 255, 255))
    img.save(image_path)
    
    # Mock thresholds to 0.99 to ensure no detection is possible
    old_thresholds = settings.grounding_dino.thresholds
    mock_thresholds = MagicMock()
    mock_thresholds.pass1 = 0.99
    mock_thresholds.pass2 = 0.99
    mock_thresholds.pass3 = 0.99
    mock_thresholds.pass4 = 0.99
    settings.grounding_dino.thresholds = mock_thresholds
    
    try:
        with pytest.raises(NoObjectDetected):
            run_detection_pipeline_stage2(job_id, image_path, "zebra")
    finally:
        settings.grounding_dino.thresholds = old_thresholds
        
    # Cleanup
    if os.path.exists(image_path):
        os.remove(image_path)

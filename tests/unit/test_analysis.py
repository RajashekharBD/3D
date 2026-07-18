import os
import json
import pytest
from PIL import Image
import io
from backend.app.services.image_service import image_service
from backend.app.utils.image_utils import analyze_image_properties, is_clahe_required
from backend.app.core.settings import settings

def create_temp_image(filename: str, color: tuple, size=(100, 100)) -> str:
    """Helper to write a temporary test image file."""
    os.makedirs("data/temp", exist_ok=True)
    file_path = os.path.join("data/temp", filename)
    img = Image.new("RGB", size, color=color)
    img.save(file_path)
    return file_path

def test_analyze_image_properties():
    # Create a bright white image
    file_path = create_temp_image("white.jpg", (255, 255, 255))
    props = analyze_image_properties(file_path)
    
    assert props["width"] == 100
    assert props["height"] == 100
    assert props["channels"] == 3
    # Brightness should be close to 1.0
    assert props["mean_brightness"] > 0.95
    # Uniform color means contrast is close to 0.0
    assert props["contrast"] < 0.05
    
    if os.path.exists(file_path):
        os.remove(file_path)

def test_clahe_decision_logic():
    # Test cases for is_clahe_required
    # Normal image: high brightness, high contrast -> False
    assert is_clahe_required({"mean_brightness": 0.50, "contrast": 0.20}) is False
    
    # Dark image: low brightness -> True
    assert is_clahe_required({"mean_brightness": 0.20, "contrast": 0.20}) is True
    
    # Low contrast image -> True
    assert is_clahe_required({"mean_brightness": 0.50, "contrast": 0.10}) is True

def test_store_analysis_metadata():
    job_id = "test-job-analysis-123"
    file_path = create_temp_image("gray.jpg", (128, 128, 128))
    
    metadata = image_service.analyze_job_image(job_id, file_path)
    
    assert metadata["job_id"] == job_id
    assert "image_properties" in metadata
    assert "clahe_required" in metadata
    
    # Check if JSON file exists and contains matching info
    dest_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
    assert os.path.exists(dest_path)
    
    with open(dest_path, "r") as f:
        data = json.load(f)
        assert data["job_id"] == job_id
        assert data["image_properties"]["width"] == 100
        
    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(dest_path):
        os.remove(dest_path)

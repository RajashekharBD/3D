import os
import pytest
from PIL import Image, ImageEnhance
from backend.app.pipeline.image_pipeline import run_image_pipeline

def create_test_image(filename: str, mode: str, size=(100, 100)) -> str:
    """Helper to generate specific image brightness patterns for test inputs."""
    os.makedirs("data/temp", exist_ok=True)
    file_path = os.path.join("data/temp", filename)
    
    if mode == "normal":
        # Split color black/white (mean brightness 0.5, high contrast 0.5)
        img = Image.new("RGB", size, color="black")
        # Draw white in the right half
        for x in range(size[0] // 2, size[0]):
            for y in range(size[1]):
                img.putpixel((x, y), (255, 255, 255))
    elif mode == "dark":
        # Low brightness color (dark green/blue color, mean brightness ~0.10)
        img = Image.new("RGB", size, color=(20, 30, 20))
    elif mode == "low_contrast":
        # Low contrast gray image (low std dev)
        img = Image.new("RGB", size, color=(120, 120, 120))
        # Add very slight noise to prevent zero std dev warning
        img.putpixel((0,0), (121,121,121))
        
    img.save(file_path)
    return file_path

def test_clahe_bypassed_on_normal_image():
    job_id = "job-clahe-bypass"
    original_path = create_test_image("normal.png", "normal")
    
    result = run_image_pipeline(job_id, original_path)
    
    assert result["success"] is True
    assert result["clahe_applied"] is False
    assert result["enhanced_image_path"] is None
    
    # Cleanup
    if os.path.exists(original_path):
        os.remove(original_path)

def test_clahe_applied_on_dark_image():
    job_id = "job-clahe-apply-dark"
    original_path = create_test_image("dark.png", "dark")
    
    result = run_image_pipeline(job_id, original_path)
    
    assert result["success"] is True
    assert result["clahe_applied"] is True
    assert result["enhanced_image_path"] is not None
    assert os.path.exists(result["enhanced_image_path"])
    
    # Verify dimensions are preserved
    with Image.open(result["enhanced_image_path"]) as img:
        assert img.size == (100, 100)
        
    # Cleanup
    if os.path.exists(original_path):
        os.remove(original_path)
    if os.path.exists(result["enhanced_image_path"]):
        os.remove(result["enhanced_image_path"])

def test_clahe_applied_on_low_contrast_image():
    job_id = "job-clahe-apply-low-contrast"
    original_path = create_test_image("low_contrast.png", "low_contrast")
    
    result = run_image_pipeline(job_id, original_path)
    
    assert result["success"] is True
    assert result["clahe_applied"] is True
    assert result["enhanced_image_path"] is not None
    assert os.path.exists(result["enhanced_image_path"])
    
    # Cleanup
    if os.path.exists(original_path):
        os.remove(original_path)
    if os.path.exists(result["enhanced_image_path"]):
        os.remove(result["enhanced_image_path"])

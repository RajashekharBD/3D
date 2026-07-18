import os
import json
import pytest
from PIL import Image
from backend.app.pipeline.detection_pipeline import run_detection_pipeline_stage1
from ai_models.florence2.caption import transform_caption_to_prompt

def test_caption_to_prompt_transformation():
    # Verify filter rules
    caption = "A black ceramic mug on a table"
    prompt = transform_caption_to_prompt(caption)
    assert prompt == "black . ceramic . mug . table"
    
    caption = "the shiny red toy car with wheels"
    prompt = transform_caption_to_prompt(caption)
    assert prompt == "shiny . red . toy . car . wheels"

@pytest.mark.skipif(os.environ.get("SKIP_HF_TESTS") == "true", reason="Skipping HuggingFace model download tests")
def test_florence2_inference():
    # 1. Create a simple red canvas image
    os.makedirs("data/temp", exist_ok=True)
    test_image_path = "data/temp/test_vlm_input.png"
    img = Image.new("RGB", (128, 128), color="red")
    img.save(test_image_path)
    
    job_id = "test-job-vlm-caption"
    
    # 2. Run the detection pipeline stage 1
    result = run_detection_pipeline_stage1(job_id, test_image_path)
    
    assert result["success"] is True
    assert len(result["caption"]) > 0
    assert len(result["detection_prompt"]) > 0
    
    # Check that metadata file is updated correctly
    metadata_path = f"outputs/metadata/{job_id}_result.json"
    assert os.path.exists(metadata_path)
    with open(metadata_path, "r") as f:
        data = json.load(f)
        assert data["caption"] == result["caption"]
        assert data["detection_prompt"] == result["detection_prompt"]
        
    # Cleanup
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
    if os.path.exists(metadata_path):
        os.remove(metadata_path)

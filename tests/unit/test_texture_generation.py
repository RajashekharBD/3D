import os
import json
import pytest
import shutil
import trimesh
from PIL import Image
from backend.app.pipeline.generation_pipeline import run_shape_generation_pipeline, run_texture_generation_pipeline
from backend.app.core.settings import settings

def create_texture_test_image(filename: str) -> str:
    """Creates a simple RGBA image with a shape in the center for texture generation test."""
    os.makedirs("data/temp", exist_ok=True)
    file_path = os.path.join("data/temp", filename)
    img = Image.new("RGBA", (100, 100), color=(0, 0, 0, 0))
    # Draw opaque blue square in the center
    for x in range(30, 70):
        for y in range(30, 70):
            img.putpixel((x, y), (0, 0, 255, 255))
    img.save(file_path)
    return file_path

def test_texture_generation_success():
    job_id = "test-job-texture-gen"
    image_path = create_texture_test_image("test_texture_input.png")
    
    # 1. Pre-init job folder and run shape generation to generate untextured model.glb
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, image_path)
    
    # Run shape generation stage
    shape_result = run_shape_generation_pipeline(job_id, image_path)
    assert shape_result["success"] is True
    
    try:
        # 2. Run the texture generation pipeline
        result = run_texture_generation_pipeline(job_id, image_path)
        
        assert result["success"] is True
        textured_path = result["textured_mesh_path"]
        assert os.path.exists(textured_path)
        
        # 3. Verify final GLB is readable and contains valid texture visuals
        mesh = trimesh.load(textured_path, file_type="glb")
        
        # Extract mesh if it loaded as a scene
        if isinstance(mesh, trimesh.Scene):
            geoms = list(mesh.geometry.values())
            assert len(geoms) > 0
            mesh = geoms[0]
            
        assert isinstance(mesh, trimesh.Trimesh)
        # Check that texture visuals are attached
        assert hasattr(mesh, "visual")
        assert isinstance(mesh.visual, trimesh.visual.TextureVisuals)
        
        # 4. Verify result.json updates
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        result_json_path = os.path.join(job_dir, "result.json")
        assert os.path.exists(result_json_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "texture_generation" in data["completed_phases"]
            assert data["artifacts"]["model"] == "model.glb"
            
    finally:
        # Cleanup
        if os.path.exists(image_path):
            os.remove(image_path)
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        final_glb_copy = os.path.join(settings.OUTPUT_DIR, "meshes", f"{job_id}_model.glb")
        if os.path.exists(final_glb_copy):
            os.remove(final_glb_copy)
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

def test_texture_generation_invalid_mesh_graceful_fail():
    job_id = "test-job-texture-fail"
    image_path = create_texture_test_image("test_texture_fail_input.png")
    
    # 1. Pre-init job folder, but do NOT create model.glb
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, image_path)
    
    try:
        with pytest.raises(FileNotFoundError):
            run_texture_generation_pipeline(job_id, image_path)
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)

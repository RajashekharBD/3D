import os
import json
import pytest
import shutil
import trimesh
from PIL import Image
from backend.app.pipeline.generation_pipeline import run_shape_generation_pipeline
from backend.app.core.settings import settings

def create_shape_test_image(filename: str) -> str:
    """Creates a simple RGBA image with a shape in the center for shape generation test."""
    os.makedirs("data/temp", exist_ok=True)
    file_path = os.path.join("data/temp", filename)
    
    # 100x100 canvas, transparent background
    img = Image.new("RGBA", (100, 100), color=(0, 0, 0, 0))
    # Draw opaque square in the center
    for x in range(30, 70):
        for y in range(30, 70):
            img.putpixel((x, y), (255, 0, 0, 255))
            
    img.save(file_path)
    return file_path

def test_shape_generation_success():
    job_id = "test-job-shape-gen"
    image_path = create_shape_test_image("test_shape_input.png")
    
    # 1. Pre-init job folder
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, image_path)
    
    try:
        # 2. Run the shape generation pipeline
        result = run_shape_generation_pipeline(job_id, image_path)
        
        assert result["success"] is True
        assert result["vertex_count"] > 0
        assert result["face_count"] > 0
        
        mesh_path = result["mesh_path"]
        assert os.path.exists(mesh_path)
        
        # 3. Verify mesh is readable and valid in trimesh
        mesh = trimesh.load(mesh_path, file_type="glb")
        assert isinstance(mesh, trimesh.Trimesh) or isinstance(mesh, trimesh.Scene)
        
        # If it loaded as a scene, get the geometry
        if isinstance(mesh, trimesh.Scene):
            geoms = list(mesh.geometry.values())
            assert len(geoms) > 0
            mesh = geoms[0]
            
        assert len(mesh.vertices) == result["vertex_count"]
        assert len(mesh.faces) == result["face_count"]
        
        # 4. Verify result.json updates
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        result_json_path = os.path.join(job_dir, "result.json")
        assert os.path.exists(result_json_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "shape_generation" in data["completed_phases"]
            assert data["artifacts"]["model"] == "model.glb"
            assert "mesh_metadata" in data
            assert data["mesh_metadata"]["vertex_count"] == result["vertex_count"]
            assert data["mesh_metadata"]["face_count"] == result["face_count"]
            
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

def test_shape_generation_invalid_input_graceful_fail():
    job_id = "test-job-shape-fail"
    invalid_path = "non_existent_image.png"
    
    with pytest.raises(Exception):
        run_shape_generation_pipeline(job_id, invalid_path)

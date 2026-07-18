import os
import json
import pytest
import shutil
import trimesh
from backend.app.pipeline.generation_pipeline import run_mesh_validation_pipeline
from backend.app.core.settings import settings

def test_mesh_validation_success():
    job_id = "test-job-mesh-val"
    
    # 1. Pre-init job folder and metadata json
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    meshes_dir = os.path.join(settings.OUTPUT_DIR, "meshes")
    os.makedirs(meshes_dir, exist_ok=True)
    
    # Save a mock untextured model in job and meshes folder
    mesh = trimesh.creation.icosphere(subdivisions=2, radius=0.5)
    
    job_model_path = os.path.join(job_dir, "model.glb")
    glb_mesh_path = os.path.join(meshes_dir, f"{job_id}_model.glb")
    mesh.export(job_model_path, file_type="glb")
    mesh.export(glb_mesh_path, file_type="glb")
    
    # Initialise result.json
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, job_model_path)
    
    try:
        # 2. Run the mesh validation pipeline
        result = run_mesh_validation_pipeline(job_id)
        
        assert result["success"] is True
        assert "stats" in result
        stats = result["stats"]
        
        assert stats["vertices"] > 0
        assert stats["triangles"] > 0
        assert "is_watertight" in stats
        
        # 3. Check result.json updates
        result_json_path = os.path.join(job_dir, "result.json")
        assert os.path.exists(result_json_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "mesh_validation" in data["completed_phases"]
            assert "mesh_validation_metadata" in data
            assert data["mesh_validation_metadata"]["vertices"] == stats["vertices"]
            assert data["mesh_validation_metadata"]["triangles"] == stats["triangles"]
            
    finally:
        # Cleanup
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        if os.path.exists(glb_mesh_path):
            os.remove(glb_mesh_path)
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

def test_mesh_validation_missing_file_graceful_fail():
    job_id = "test-job-mesh-val-fail"
    
    with pytest.raises(FileNotFoundError):
        run_mesh_validation_pipeline(job_id)

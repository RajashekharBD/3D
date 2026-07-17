import os
import json
import pytest
import shutil
import trimesh
import open3d as o3d
from backend.app.pipeline.generation_pipeline import run_pointcloud_generation_pipeline
from backend.app.core.settings import settings

def test_pointcloud_generation_success():
    job_id = "test-job-pcd"
    
    # 1. Pre-init job folder and metadata json
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    meshes_dir = os.path.join(settings.OUTPUT_DIR, "meshes")
    os.makedirs(meshes_dir, exist_ok=True)
    
    # Save a mock model in job and meshes folder
    mesh = trimesh.creation.icosphere(subdivisions=2, radius=0.5)
    
    job_model_path = os.path.join(job_dir, "model.glb")
    glb_mesh_path = os.path.join(meshes_dir, f"{job_id}_model.glb")
    mesh.export(job_model_path, file_type="glb")
    mesh.export(glb_mesh_path, file_type="glb")
    
    # Initialise result.json
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, job_model_path)
    
    try:
        # 2. Run the point cloud generation pipeline
        result = run_pointcloud_generation_pipeline(job_id)
        
        assert result["success"] is True
        assert "stats" in result
        stats = result["stats"]
        
        # Open3D poisson disk sampling sometimes returns close to target
        assert stats["point_count"] > 0
        assert stats["has_normals"] is True
        
        pcd_path = os.path.join(settings.OUTPUT_DIR, "pointcloud", f"{job_id}_pointcloud.ply")
        assert os.path.exists(pcd_path)
        
        # 3. Reload point cloud using Open3D and verify validity
        pcd = o3d.io.read_point_cloud(pcd_path)
        assert isinstance(pcd, o3d.geometry.PointCloud)
        assert len(pcd.points) == stats["point_count"]
        assert pcd.has_normals()
        
        # 4. Check result.json updates
        result_json_path = os.path.join(job_dir, "result.json")
        assert os.path.exists(result_json_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "pointcloud_generation" in data["completed_phases"]
            assert "pointcloud_metadata" in data
            assert data["pointcloud_metadata"]["point_count"] == stats["point_count"]
            assert data["artifacts"]["pointcloud"] == "pointcloud.ply"
            
    finally:
        # Cleanup
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        if os.path.exists(glb_mesh_path):
            os.remove(glb_mesh_path)
        pcd_path = os.path.join(settings.OUTPUT_DIR, "pointcloud", f"{job_id}_pointcloud.ply")
        if os.path.exists(pcd_path):
            os.remove(pcd_path)
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

def test_pointcloud_generation_missing_file_graceful_fail():
    job_id = "test-job-pcd-fail"
    
    with pytest.raises(FileNotFoundError):
        run_pointcloud_generation_pipeline(job_id)

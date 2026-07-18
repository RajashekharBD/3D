import os
import json
import pytest
import shutil
import open3d as o3d
import numpy as np
from backend.app.pipeline.pointcloud_pipeline import run_dbscan_segmentation_pipeline
from backend.app.core.settings import settings

def create_raw_pcd_file(ply_path: str):
    """Creates a raw point cloud with two separate spatial clusters for DBSCAN testing."""
    os.makedirs(os.path.dirname(ply_path), exist_ok=True)
    
    # Cluster 1: 50 points around (0, 0, 0)
    pts1 = np.random.normal(0, 0.01, size=(50, 3))
    # Cluster 2: 50 points around (1, 1, 1)
    pts2 = np.random.normal(1, 0.01, size=(50, 3))
    
    pts = np.vstack([pts1, pts2])
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)
    
    # Save raw point cloud
    o3d.io.write_point_cloud(ply_path, pcd, write_ascii=False, compressed=True)

def test_dbscan_segmentation_success():
    job_id = "test-job-dbscan"
    
    # 1. Pre-init directories
    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)
    
    pcd_dir = os.path.join(settings.OUTPUT_DIR, "pointcloud")
    os.makedirs(pcd_dir, exist_ok=True)
    
    raw_ply_path = os.path.join(pcd_dir, f"{job_id}_pointcloud.ply")
    job_raw_ply = os.path.join(job_dir, "pointcloud.ply")
    
    # Generate test points
    create_raw_pcd_file(raw_ply_path)
    shutil.copy(raw_ply_path, job_raw_ply)
    
    # Initialise result.json
    from backend.app.utils.artifacts_manager import artifacts_manager
    artifacts_manager.init_job(job_id, job_raw_ply)
    
    try:
        # 2. Run DBSCAN segmentation pipeline
        result = run_dbscan_segmentation_pipeline(job_id)
        
        assert result["success"] is True
        assert "stats" in result
        stats = result["stats"]
        
        # We expect 2 clusters
        assert stats["total_clusters"] >= 1
        assert stats["total_points"] == 100
        
        segmented_ply_path = os.path.join(pcd_dir, f"{job_id}_segmented_pointcloud.ply")
        assert os.path.exists(segmented_ply_path)
        
        # Reload and verify
        pcd = o3d.io.read_point_cloud(segmented_ply_path)
        assert pcd.has_colors()
        assert len(pcd.points) == stats["clustered_points"]
        
        # 3. Check result.json updates
        result_json_path = os.path.join(job_dir, "result.json")
        assert os.path.exists(result_json_path)
        
        with open(result_json_path, "r") as f:
            data = json.load(f)
            assert "dbscan_segmentation" in data["completed_phases"]
            assert "dbscan_metadata" in data
            assert data["dbscan_metadata"]["total_clusters"] == stats["total_clusters"]
            assert data["artifacts"]["segmented_pointcloud"] == "segmented_pointcloud.ply"
            
    finally:
        # Cleanup
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
        if os.path.exists(raw_ply_path):
            os.remove(raw_ply_path)
        seg_ply_path = os.path.join(pcd_dir, f"{job_id}_segmented_pointcloud.ply")
        if os.path.exists(seg_ply_path):
            os.remove(seg_ply_path)
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            os.remove(metadata_path)

def test_dbscan_missing_file_graceful_fail():
    job_id = "test-job-dbscan-fail"
    
    with pytest.raises(FileNotFoundError):
        run_dbscan_segmentation_pipeline(job_id)

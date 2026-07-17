import os
import time
import json
import shutil
from backend.app.core.settings import settings
from backend.app.utils.logger import logger
from backend.app.utils.pointcloud_utils import sample_pointcloud_from_mesh, segment_pointcloud_dbscan
from backend.app.utils.artifacts_manager import artifacts_manager

class PointcloudService:
    def generate_job_pointcloud(self, job_id: str) -> dict:
        """Generates a dense PLY point cloud from the job's validated GLB mesh.
        
        Saves outputs and updates result metadata.
        """
        start_time = time.time()
        logger.info(f"Executing Point Cloud Generation Service for Job ID: {job_id}")
        
        # Paths
        meshes_dir = os.path.join(settings.OUTPUT_DIR, "meshes")
        glb_mesh_path = os.path.join(meshes_dir, f"{job_id}_model.glb")
        
        pointcloud_dir = os.path.join(settings.OUTPUT_DIR, "pointcloud")
        os.makedirs(pointcloud_dir, exist_ok=True)
        ply_dest_path = os.path.join(pointcloud_dir, f"{job_id}_pointcloud.ply")
        
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        job_ply_path = os.path.join(job_dir, "pointcloud.ply")
        
        # Fallback to job directory model.glb if missing in meshes folder
        if not os.path.exists(glb_mesh_path):
             job_model_path = os.path.join(job_dir, "model.glb")
             if os.path.exists(job_model_path):
                 logger.warning("Validated mesh not found in outputs/meshes/. Using job folder copy.")
                 os.makedirs(meshes_dir, exist_ok=True)
                 shutil.copy(job_model_path, glb_mesh_path)
             else:
                 raise FileNotFoundError(f"Source model.glb not found for job: {job_id}")
                 
        # Target point count
        target_count = getattr(settings.pointcloud, "target_points", 100000)
        
        # Run sampler
        stats = sample_pointcloud_from_mesh(glb_mesh_path, ply_dest_path, target_count)
        
        # Copy to self-contained job outputs folder
        os.makedirs(job_dir, exist_ok=True)
        shutil.copy(ply_dest_path, job_ply_path)
        logger.info(f"Copied point cloud to job directory: {job_ply_path}")
        
        generation_time = time.time() - start_time
        stats["generation_time_sec"] = float(generation_time)
        
        # Update result.json completed phases and artifact
        artifacts_manager.add_file_artifact(job_id, "pointcloud", job_ply_path, "pointcloud.ply")
        artifacts_manager.add_completed_phase(job_id, "pointcloud_generation")
        
        # Append detailed pointcloud metadata to result.json
        result_json_path = os.path.join(job_dir, "result.json")
        if os.path.exists(result_json_path):
            try:
                with open(result_json_path, "r") as f:
                    res_data = json.load(f)
                res_data["pointcloud_metadata"] = stats
                with open(result_json_path, "w") as f:
                    json.dump(res_data, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append pointcloud stats to result.json: {js_err}")
                
        # Update metadata JSON file
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                meta["stage"] = "Point Cloud Generation"
                meta["pointcloud_path"] = ply_dest_path
                meta["point_count"] = stats["point_count"]
                meta["pointcloud_has_colors"] = stats["has_colors"]
                meta["pointcloud_has_normals"] = stats["has_normals"]
                with open(metadata_path, "w") as f:
                    json.dump(meta, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append pointcloud properties in result metadata: {js_err}")
                
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: Point Cloud Generation\n"
            f"Status: Success\n"
            f"Time: {generation_time:.2f} Seconds\n"
            f"Point Count: {stats['point_count']}\n"
            f"Has Colors: {stats['has_colors']}\n"
            f"Has Normals: {stats['has_normals']}\n"
            f"Output PLY: {ply_dest_path}\n"
        )
        
        return stats

    def segment_job_pointcloud_dbscan(self, job_id: str) -> dict:
        """Applies DBSCAN segmentation on the raw point cloud for the given job.
        
        Saves segmented PLY and updates result metadata.
        """
        start_time = time.time()
        logger.info(f"Executing DBSCAN Segmentation Service for Job ID: {job_id}")
        
        # Paths
        pointcloud_dir = os.path.join(settings.OUTPUT_DIR, "pointcloud")
        ply_src_path = os.path.join(pointcloud_dir, f"{job_id}_pointcloud.ply")
        ply_dest_path = os.path.join(pointcloud_dir, f"{job_id}_segmented_pointcloud.ply")
        
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        job_ply_path = os.path.join(job_dir, "segmented_pointcloud.ply")
        
        # Ensure source point cloud exists
        if not os.path.exists(ply_src_path):
             # Try fallback to job directory pointcloud.ply
             job_raw_ply = os.path.join(job_dir, "pointcloud.ply")
             if os.path.exists(job_raw_ply):
                 logger.warning("Raw point cloud not found in outputs/pointcloud/. Copying from job folder.")
                 os.makedirs(pointcloud_dir, exist_ok=True)
                 shutil.copy(job_raw_ply, ply_src_path)
             else:
                 raise FileNotFoundError(f"Source pointcloud.ply not found for job: {job_id}")
                 
        # Run DBSCAN segmentation
        eps = settings.dbscan.eps
        min_points = settings.dbscan.min_points
        remove_outliers = settings.dbscan.remove_outliers
        
        stats = segment_pointcloud_dbscan(ply_src_path, ply_dest_path, eps, min_points, remove_outliers)
        
        # Copy to self-contained job outputs folder
        shutil.copy(ply_dest_path, job_ply_path)
        logger.info(f"Copied segmented point cloud to job directory: {job_ply_path}")
        
        execution_time = time.time() - start_time
        stats["execution_time_sec"] = float(execution_time)
        
        # Update result.json completed phases and artifact
        artifacts_manager.add_file_artifact(job_id, "segmented_pointcloud", job_ply_path, "segmented_pointcloud.ply")
        artifacts_manager.add_completed_phase(job_id, "dbscan_segmentation")
        
        # Append detailed DBSCAN metadata to result.json
        result_json_path = os.path.join(job_dir, "result.json")
        if os.path.exists(result_json_path):
            try:
                with open(result_json_path, "r") as f:
                    res_data = json.load(f)
                res_data["dbscan_metadata"] = stats
                with open(result_json_path, "w") as f:
                    json.dump(res_data, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append DBSCAN stats to result.json: {js_err}")
                
        # Update metadata JSON file
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                meta["stage"] = "DBSCAN Segmentation"
                meta["segmented_pointcloud_path"] = ply_dest_path
                meta["dbscan_total_clusters"] = stats["total_clusters"]
                meta["dbscan_outliers"] = stats["outlier_points"]
                meta["dbscan_eps"] = stats["eps"]
                meta["dbscan_min_points"] = stats["min_points"]
                with open(metadata_path, "w") as f:
                    json.dump(meta, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append DBSCAN properties in result metadata: {js_err}")
                
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: DBSCAN Segmentation\n"
            f"Status: Success\n"
            f"Time: {execution_time:.2f} Seconds\n"
            f"Clusters: {stats['total_clusters']}\n"
            f"Outliers: {stats['outlier_points']}\n"
            f"Segmented Output PLY: {ply_dest_path}\n"
        )
        
        return stats

pointcloud_service = PointcloudService()

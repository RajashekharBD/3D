import time
from backend.app.utils.logger import logger

def run_dbscan_segmentation_pipeline(job_id: str) -> dict:
    """Executes Stage 9 of the pipeline: DBSCAN Point Cloud Segmentation (Phase 18).
    
    Loads the raw point cloud, performs DBSCAN clustering, filters outliers,
    colors segments, and saves outputs.
    """
    start_time = time.time()
    logger.info(f"Starting DBSCAN Segmentation Pipeline for Job ID: {job_id}")
    
    try:
        from backend.app.services.pointcloud_service import pointcloud_service
        stats = pointcloud_service.segment_job_pointcloud_dbscan(job_id)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Log structured execution details to logs/pipeline.log
        logger.info(
            f"\nStage: DBSCAN Segmentation Pipeline\n"
            f"Status: Success\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Segmented Stats: {stats}\n"
        )
        
        return {
            "success": True,
            "duration_sec": duration,
            "stats": stats
        }
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        logger.error(
            f"\nStage: DBSCAN Segmentation Pipeline\n"
            f"Status: Failed\n"
            f"Time: {duration:.2f} Seconds\n"
            f"Error: {str(e)}\n"
        )
        raise e

import os
import shutil
import logging
from fastapi import HTTPException
from backend.app.core.database import db
from backend.app.core.settings import settings
from backend.app.utils.artifacts_manager import artifacts_manager

logger = logging.getLogger("SingleImage3D")

class HistoryController:
    def get_history(self, current_user: dict, filename: str = None, status: str = None, sort_by: str = "newest", page: int = 1) -> dict:
        """Retrieves job processing history for the authenticated user."""
        user_id = current_user["id"]
        limit = 20
        offset = (page - 1) * limit

        if not db.is_enabled:
            # Fallback to local files if Supabase is disabled
            local_jobs = []
            if os.path.exists(settings.OUTPUT_DIR):
                for job_id in os.listdir(settings.OUTPUT_DIR):
                    job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
                    if os.path.isdir(job_dir):
                        result_path = os.path.join(job_dir, "result.json")
                        if os.path.exists(result_path):
                            try:
                                data = artifacts_manager._read_result_json(job_id)
                                status_val = data.get("status", "running")
                                filename_val = data.get("original_filename", "uploaded_file.png")
                                local_jobs.append({
                                    "job_id": job_id,
                                    "user_id": user_id,
                                    "original_filename": filename_val,
                                    "status": status_val,
                                    "started_at": data.get("started_at", "now()"),
                                    "completed_at": data.get("completed_at"),
                                    "processing_duration_seconds": data.get("processing_duration_seconds", 0.0),
                                    "model_generated": "model" in data.get("artifacts", {}),
                                    "pointcloud_generated": "pointcloud" in data.get("artifacts", {}),
                                    "pipeline_version": "2.0.0",
                                    "error_message": data.get("error")
                                })
                            except Exception as e:
                                logger.error(f"Error reading local job {job_id}: {e}")
            
            # Apply in-memory filtering for local mock fallback
            if filename:
                local_jobs = [j for j in local_jobs if filename.lower() in j["original_filename"].lower()]
            if status:
                local_jobs = [j for j in local_jobs if j["status"] == status]
            
            local_jobs.sort(key=lambda j: j["started_at"], reverse=(sort_by == "newest"))
            
            total = len(local_jobs)
            paginated_jobs = local_jobs[offset : offset + limit]
            return {
                "jobs": paginated_jobs,
                "total": total,
                "page": page,
                "pages": (total + limit - 1) // limit if total > 0 else 1
            }

        # Query database via Supabase PostgREST
        try:
            query = db.get_client().table("jobs").select("*", count="exact").eq("user_id", user_id).eq("is_deleted", False)
            
            if filename:
                query = query.ilike("original_filename", f"%{filename}%")
            if status:
                query = query.eq("status", status)
                
            order_asc = (sort_by == "oldest")
            query = query.order("started_at", desc=not order_asc)
            
            # Fetch slice for pagination
            res = query.range(offset, offset + limit - 1).execute()
            total = res.count if res.count is not None else len(res.data)
            
            return {
                "jobs": res.data,
                "total": total,
                "page": page,
                "pages": (total + limit - 1) // limit if total > 0 else 1
            }
        except Exception as e:
            logger.error(f"Failed to fetch job history from database: {e}")
            raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

    def get_job_detail(self, job_id: str, current_user: dict) -> dict:
        """Retrieves details and artifact metadata for a specific job."""
        user_id = current_user["id"]
        
        if not db.is_enabled:
            # Fallback to local files
            job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
            if not os.path.exists(job_dir):
                raise HTTPException(status_code=404, detail="Job not found.")
            data = artifacts_manager._read_result_json(job_id)
            return {
                "job": {
                    "job_id": job_id,
                    "user_id": user_id,
                    "original_filename": "uploaded_file.png",
                    "status": data.get("status", "running"),
                    "model_generated": "model" in data.get("artifacts", {}),
                    "pointcloud_generated": "pointcloud" in data.get("artifacts", {})
                },
                "artifacts": [
                    {"artifact_type": k, "file_path": f"outputs/{job_id}/{v}"}
                    for k, v in data.get("artifacts", {}).items()
                ]
            }

        try:
            # Fetch job details
            job_res = db.get_client().table("jobs").select("*").eq("job_id", job_id).eq("is_deleted", False).execute()
            if not job_res.data:
                raise HTTPException(status_code=404, detail="Job not found.")
            
            job = job_res.data[0]
            if job["user_id"] != user_id:
                raise HTTPException(status_code=403, detail="Forbidden: You do not own this job.")
                
            # Fetch artifacts details
            art_res = db.get_client().table("artifacts").select("*").eq("job_id", job_id).execute()
            return {
                "job": job,
                "artifacts": art_res.data
            }
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            logger.error(f"Failed to fetch job detail: {e}")
            raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

    def delete_job(self, job_id: str, current_user: dict) -> dict:
        """Performs soft delete on database record and cleans up local storage folder."""
        user_id = current_user["id"]

        if db.is_enabled:
            try:
                # Enforce ownership check
                job_res = db.get_client().table("jobs").select("user_id").eq("job_id", job_id).execute()
                if not job_res.data:
                    raise HTTPException(status_code=404, detail="Job not found.")
                if job_res.data[0]["user_id"] != user_id:
                    raise HTTPException(status_code=403, detail="Forbidden: You do not own this job.")
                
                # Perform soft delete in database
                db.get_client().table("jobs").update({"is_deleted": True}).eq("job_id", job_id).execute()
            except Exception as e:
                if isinstance(e, HTTPException):
                    raise
                logger.error(f"Failed to soft delete job in Database: {e}")
                raise HTTPException(status_code=500, detail=f"Database soft delete failed: {e}")

        # Clean up local output folder
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        if os.path.exists(job_dir):
            try:
                shutil.rmtree(job_dir)
                logger.info(f"Cleaned up local folder for job: {job_id}")
            except Exception as e:
                logger.error(f"Failed to delete local folder for job {job_id}: {e}")

        return {"success": True, "message": f"Job {job_id} successfully deleted."}

history_controller = HistoryController()

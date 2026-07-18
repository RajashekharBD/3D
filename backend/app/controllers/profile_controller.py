import logging
from fastapi import HTTPException
from backend.app.core.database import db

logger = logging.getLogger("SingleImage3D")

class ProfileController:
    def get_profile(self, current_user: dict) -> dict:
        """Retrieves user profile and computes AI pipeline usage statistics."""
        user_id = current_user["id"]
        email = current_user["email"]

        if not db.is_enabled:
            # Local fallback stats
            return {
                "profile": {
                    "id": user_id,
                    "email": email,
                    "created_at": "now()",
                    "last_login": "now()"
                },
                "statistics": {
                    "total_uploads": 0,
                    "completed_jobs": 0,
                    "failed_jobs": 0,
                    "models_generated": 0,
                    "pointclouds_generated": 0,
                    "average_processing_time": 0.0,
                    "last_upload": None
                }
            }

        try:
            if user_id == "d0000000-0000-0000-0000-000000000000":
                return {
                    "profile": {"id": user_id, "email": email, "created_at": "now()", "last_login": "now()"},
                    "statistics": {
                        "total_uploads": 0,
                        "completed_jobs": 0,
                        "failed_jobs": 0,
                        "models_generated": 0,
                        "pointclouds_generated": 0,
                        "average_processing_time": 0.0,
                        "last_upload": None
                    }
                }

            # Get profile info
            prof_res = db.get_client().table("profiles").select("*").eq("id", user_id).execute()
            if not prof_res.data:
                db.get_client().table("profiles").insert({
                    "id": user_id,
                    "email": email,
                    "last_login": "now()"
                }).execute()
                prof_res = db.get_client().table("profiles").select("*").eq("id", user_id).execute()
            
            profile = prof_res.data[0] if prof_res.data else {
                "id": user_id,
                "email": email,
                "created_at": "now()",
                "last_login": "now()"
            }

            # Fetch all user jobs to compute statistics in Python
            jobs_res = db.get_client().table("jobs").select("*").eq("user_id", user_id).eq("is_deleted", False).execute()
            jobs = jobs_res.data

            total_uploads = len(jobs)
            completed_jobs = sum(1 for j in jobs if j.get("status") == "completed")
            failed_jobs = sum(1 for j in jobs if j.get("status") == "failed")
            models_generated = sum(1 for j in jobs if j.get("model_generated"))
            pointclouds_generated = sum(1 for j in jobs if j.get("pointcloud_generated"))
            
            durations = [j.get("processing_duration_seconds") for j in jobs if j.get("processing_duration_seconds") is not None]
            avg_duration = sum(durations) / len(durations) if durations else 0.0
            
            last_upload = max([j.get("started_at") for j in jobs]) if jobs else None

            return {
                "profile": profile,
                "statistics": {
                    "total_uploads": total_uploads,
                    "completed_jobs": completed_jobs,
                    "failed_jobs": failed_jobs,
                    "models_generated": models_generated,
                    "pointclouds_generated": pointclouds_generated,
                    "average_processing_time": avg_duration,
                    "last_upload": last_upload
                }
            }
        except Exception as e:
            logger.error(f"Failed to fetch profile statistics: {e}")
            raise HTTPException(status_code=500, detail=f"Database query failed: {e}")

profile_controller = ProfileController()

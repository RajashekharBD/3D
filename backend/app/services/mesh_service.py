import os
import json
import shutil
from backend.app.core.settings import settings
from backend.app.utils.logger import logger
from backend.app.utils.mesh_utils import validate_and_orient_mesh
from backend.app.utils.artifacts_manager import artifacts_manager

class MeshService:
    def validate_job_mesh(self, job_id: str) -> dict:
        """Validates and aligns normals for the job's textured GLB file using Open3D.
        
        Saves changes and updates result metadata.
        """
        logger.info(f"Executing Mesh Validation Service for Job ID: {job_id}")
        
        # Paths
        meshes_dir = os.path.join(settings.OUTPUT_DIR, "meshes")
        glb_mesh_path = os.path.join(meshes_dir, f"{job_id}_model.glb")
        job_dir = os.path.join(settings.OUTPUT_DIR, job_id)
        job_model_path = os.path.join(job_dir, "model.glb")
        
        # Ensure final textured GLB exists
        if not os.path.exists(glb_mesh_path):
             # Try fallback to job directory model.glb
             if os.path.exists(job_model_path):
                 logger.warning("Textured mesh not found in outputs/meshes/. Copying from job folder.")
                 os.makedirs(meshes_dir, exist_ok=True)
                 shutil.copy(job_model_path, glb_mesh_path)
             else:
                 raise FileNotFoundError(f"Textured model.glb not found for job: {job_id}")
                 
        # Run Open3D validation and normal alignment
        stats = validate_and_orient_mesh(glb_mesh_path)
        
        # Overwrite the job folder copy with the validated mesh
        shutil.copy(glb_mesh_path, job_model_path)
        logger.info(f"Overwrote job directory model copy with validated mesh: {job_model_path}")
        
        # Update result.json completed phases and artifact
        artifacts_manager.add_file_artifact(job_id, "model", job_model_path, "model.glb")
        artifacts_manager.add_completed_phase(job_id, "mesh_validation")
        
        # Append detailed mesh statistics to result.json
        result_json_path = os.path.join(job_dir, "result.json")
        if os.path.exists(result_json_path):
            try:
                with open(result_json_path, "r") as f:
                    res_data = json.load(f)
                res_data["mesh_validation_metadata"] = stats
                with open(result_json_path, "w") as f:
                    json.dump(res_data, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append mesh stats to result.json: {js_err}")
                
        # Update metadata JSON file
        metadata_path = os.path.join(settings.OUTPUT_DIR, "metadata", f"{job_id}_result.json")
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, "r") as f:
                    meta = json.load(f)
                meta["stage"] = "Open3D Mesh Validation"
                meta["mesh_validation"] = stats
                with open(metadata_path, "w") as f:
                    json.dump(meta, f, indent=4)
            except Exception as js_err:
                logger.error(f"Failed to append validation stats in result metadata: {js_err}")
                
        return stats

mesh_service = MeshService()

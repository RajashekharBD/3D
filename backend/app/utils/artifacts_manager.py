import os
import json
import shutil
from PIL import Image
from backend.app.core.settings import settings
from backend.app.utils.logger import logger

class JobArtifactsManager:
    def _get_job_dir(self, job_id: str) -> str:
        """Returns path to the job's outputs folder: outputs/<job_id>/"""
        return os.path.join(settings.OUTPUT_DIR, job_id)

    def _get_result_json_path(self, job_id: str) -> str:
        """Returns path to the job's result.json: outputs/<job_id>/result.json"""
        return os.path.join(self._get_job_dir(job_id), "result.json")

    def _read_result_json(self, job_id: str) -> dict:
        """Reads result.json for the job, returning a default structure if not found."""
        path = self._get_result_json_path(job_id)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to read result.json for job {job_id}: {e}")
        
        return {
            "job_id": job_id,
            "status": "running",
            "completed_phases": [],
            "artifacts": {}
        }

    def _write_result_json(self, job_id: str, data: dict) -> None:
        """Writes the updated dict to outputs/<job_id>/result.json"""
        path = self._get_result_json_path(job_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with open(path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to write result.json for job {job_id}: {e}")

    def init_job(self, job_id: str, original_image_path: str) -> None:
        """Initializes job directory and saves original.png + initial result.json."""
        job_dir = self._get_job_dir(job_id)
        os.makedirs(job_dir, exist_ok=True)

        # Convert original image to PNG and save to outputs/<job_id>/original.png
        dest_original_path = os.path.join(job_dir, "original.png")
        try:
            with Image.open(original_image_path) as img:
                img.save(dest_original_path, "PNG")
        except Exception as e:
            logger.warning(f"Could not convert/save original image as PNG: {e}. Performing raw copy instead.")
            shutil.copy(original_image_path, dest_original_path)

        # Write initial result.json
        data = {
            "job_id": job_id,
            "status": "running",
            "completed_phases": ["upload"],
            "artifacts": {
                "original": "original.png"
            }
        }
        self._write_result_json(job_id, data)
        logger.info(f"Initialized outputs directory and result.json for Job: {job_id}")

    def add_completed_phase(self, job_id: str, phase_name: str) -> None:
        """Appends a phase name to completed_phases in result.json if not present."""
        data = self._read_result_json(job_id)
        if phase_name not in data["completed_phases"]:
            data["completed_phases"].append(phase_name)
            self._write_result_json(job_id, data)

    def add_file_artifact(self, job_id: str, artifact_key: str, source_path: str, dest_filename: str) -> None:
        """Copies an artifact file to outputs/<job_id>/dest_filename and updates result.json."""
        if not os.path.exists(source_path):
            logger.warning(f"Source artifact file not found: {source_path}")
            return

        job_dir = self._get_job_dir(job_id)
        dest_path = os.path.join(job_dir, dest_filename)
        
        try:
            # Compare normalized absolute paths to avoid copying a file onto itself
            if os.path.abspath(source_path) != os.path.abspath(dest_path):
                shutil.copy(source_path, dest_path)
            # Update result.json
            data = self._read_result_json(job_id)
            data["artifacts"][artifact_key] = dest_filename
            self._write_result_json(job_id, data)
            logger.info(f"Saved artifact '{artifact_key}' to {dest_path}")
        except Exception as e:
            logger.error(f"Failed to save file artifact {artifact_key} for job {job_id}: {e}")

    def add_text_artifact(self, job_id: str, artifact_key: str, text_content: str, dest_filename: str) -> None:
        """Writes text content to outputs/<job_id>/dest_filename and updates result.json."""
        job_dir = self._get_job_dir(job_id)
        dest_path = os.path.join(job_dir, dest_filename)
        
        try:
            with open(dest_path, "w") as f:
                f.write(text_content)
            # Update result.json
            data = self._read_result_json(job_id)
            data["artifacts"][artifact_key] = dest_filename
            self._write_result_json(job_id, data)
            logger.info(f"Saved text artifact '{artifact_key}' to {dest_path}")
        except Exception as e:
            logger.error(f"Failed to save text artifact {artifact_key} for job {job_id}: {e}")

    def update_status(self, job_id: str, status: str) -> None:
        """Updates job status (e.g. 'running', 'completed', 'failed')."""
        data = self._read_result_json(job_id)
        data["status"] = status
        self._write_result_json(job_id, data)

artifacts_manager = JobArtifactsManager()

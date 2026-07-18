import os
import json
from backend.app.utils.validators import validate_image_file_path
from backend.app.utils.image_utils import analyze_image_properties, is_clahe_required
from backend.app.core.settings import settings

class ImageService:
    def validate_job_image(self, file_path: str) -> None:
        """Orchestrates image file validation for a given local file path (Phase 6)."""
        validate_image_file_path(file_path)

    def analyze_job_image(self, job_id: str, file_path: str) -> dict:
        """Performs property analysis and evaluates if CLAHE is required (Phase 7).
        
        Saves the analysis properties into outputs/metadata/<job_id>_result.json.
        """
        # Calculate image properties
        props = analyze_image_properties(file_path)
        
        # Load thresholds from configuration settings
        limits = settings.image_processing.image
        clahe_needed = is_clahe_required(
            props,
            brightness_threshold=limits.brightness_threshold,
            contrast_threshold=limits.contrast_threshold
        )
        
        # Structure metadata report
        metadata = {
            "job_id": job_id,
            "status": "success",
            "stage": "Image Analysis",
            "image_properties": props,
            "clahe_required": clahe_needed
        }
        
        # Save to outputs/metadata/<job_id>_result.json
        metadata_dir = os.path.join(settings.OUTPUT_DIR, "metadata")
        os.makedirs(metadata_dir, exist_ok=True)
        
        dest_path = os.path.join(metadata_dir, f"{job_id}_result.json")
        with open(dest_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        return metadata

image_service = ImageService()

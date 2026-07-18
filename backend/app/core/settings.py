import os
import yaml
from typing import List
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

def load_yaml_config(filename: str) -> dict:
    """Helper to load a YAML config from configs/ directory."""
    path = os.path.join("configs", filename)
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load config {path}: {e}")
    return {}

# Define schemas for each config section

class ApplicationSettings(BaseModel):
    name: str = "Single Image 3D System"
    version: str = "1.0.0"
    debug: bool = True
    max_upload_size_mb: int = 25
    allowed_extensions: List[str] = ["jpg", "jpeg", "png", "webp", "bmp"]

class ImageSettings(BaseModel):
    brightness_threshold: float = 0.30
    contrast_threshold: float = 0.15
    apply_clahe: bool = True
    max_width: int = 6000
    max_height: int = 6000
    min_width: int = 10
    min_height: int = 10
    low_memory_resize: bool = True
    target_size: int = 1024

class ClaheSettings(BaseModel):
    clip_limit: float = 2.0
    tile_grid_size: int = 8

class ImageProcessingSettings(BaseModel):
    image: ImageSettings = ImageSettings()
    clahe: ClaheSettings = ClaheSettings()

class Florence2Settings(BaseModel):
    device: str = "cuda"
    precision: str = "float16"
    max_tokens: int = 64
    temperature: float = 0.0
    beam_search: bool = True

class GroundingDinoThresholds(BaseModel):
    pass1: float = 0.20
    pass2: float = 0.20
    pass3: float = 0.15
    pass4: float = 0.10

class GroundingDinoSettings(BaseModel):
    thresholds: GroundingDinoThresholds = GroundingDinoThresholds()
    max_retries: int = 4

class Sam2Settings(BaseModel):
    multimask_output: bool = True
    choose_best_iou: bool = True
    device: str = "cuda"

class RembgSettings(BaseModel):
    use_gpu: bool = True
    output_format: str = "RGBA"

class Hunyuan3DSettings(BaseModel):
    shape_steps: int = 10
    guidance_scale: float = 5.5
    texture_steps: int = 5
    texture_resolution: int = 256
    export_format: str = "glb"
    octree_resolution: int = 128
    use_fp16: bool = True
    cpu_offload: bool = True
    sequential_cpu_offload: bool = True
    attention_slicing: bool = True
    vae_slicing: bool = True
    vae_tiling: bool = True
    lazy_loading: bool = True
    retry_on_oom: bool = True

class PointCloudSettings(BaseModel):
    target_points: int = 100000
    estimate_normals: bool = True
    radius: float = 0.05
    max_neighbors: int = 30
    orient_normals: bool = True

class DbscanSettings(BaseModel):
    eps: float = 0.05
    min_points: int = 50
    remove_outliers: bool = True

class FrontendSettings(BaseModel):
    polling_interval: int = 2000
    max_preview_size: int = 1200
    enable_dark_mode: bool = False

# Main settings class

class Settings(BaseSettings):
    # Base Env variables
    APP_NAME: str = "SingleImage3D"
    APP_ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    CUDA_DEVICE: int = 0
    OUTPUT_DIR: str = "outputs"
    TEMP_DIR: str = "data/temp"
    MAX_UPLOAD_SIZE_MB: int = 25
    DELETE_TEMP_FILES: bool = True

    # Supabase configurations
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""

    # YAML loaded configurations
    app: ApplicationSettings = ApplicationSettings()
    image_processing: ImageProcessingSettings = ImageProcessingSettings()
    florence2: Florence2Settings = Florence2Settings()
    grounding_dino: GroundingDinoSettings = GroundingDinoSettings()
    sam2: Sam2Settings = Sam2Settings()
    rembg: RembgSettings = RembgSettings()
    hunyuan3d: Hunyuan3DSettings = Hunyuan3DSettings()
    pointcloud: PointCloudSettings = PointCloudSettings()
    dbscan: DbscanSettings = DbscanSettings()
    frontend: FrontendSettings = FrontendSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def __init__(self, **kwargs):
        # Load from files first
        app_dict = load_yaml_config("app.yaml").get("application", {})
        ip_dict = load_yaml_config("image_processing.yaml")
        f2_dict = load_yaml_config("florence2.yaml").get("florence2", {})
        gd_dict = load_yaml_config("grounding_dino.yaml").get("grounding_dino", {})
        sam2_dict = load_yaml_config("sam2.yaml").get("sam2", {})
        rembg_dict = load_yaml_config("rembg.yaml").get("rembg", {})
        h3d_dict = load_yaml_config("hunyuan3d.yaml").get("hunyuan3d", {})
        pc_dict = load_yaml_config("pointcloud.yaml").get("pointcloud", {})
        dbscan_dict = load_yaml_config("dbscan.yaml").get("dbscan", {})
        fe_dict = load_yaml_config("frontend.yaml").get("frontend", {})

        # Merge YAML dicts into default model instances
        kwargs["app"] = ApplicationSettings(**app_dict) if app_dict else ApplicationSettings()
        kwargs["image_processing"] = ImageProcessingSettings(**ip_dict) if ip_dict else ImageProcessingSettings()
        kwargs["florence2"] = Florence2Settings(**f2_dict) if f2_dict else Florence2Settings()
        kwargs["grounding_dino"] = GroundingDinoSettings(**gd_dict) if gd_dict else GroundingDinoSettings()
        kwargs["sam2"] = Sam2Settings(**sam2_dict) if sam2_dict else Sam2Settings()
        kwargs["rembg"] = RembgSettings(**rembg_dict) if rembg_dict else RembgSettings()
        kwargs["hunyuan3d"] = Hunyuan3DSettings(**h3d_dict) if h3d_dict else Hunyuan3DSettings()
        kwargs["pointcloud"] = PointCloudSettings(**pc_dict) if pc_dict else PointCloudSettings()
        kwargs["dbscan"] = DbscanSettings(**dbscan_dict) if dbscan_dict else DbscanSettings()
        kwargs["frontend"] = FrontendSettings(**fe_dict) if fe_dict else FrontendSettings()

        super().__init__(**kwargs)

settings = Settings()

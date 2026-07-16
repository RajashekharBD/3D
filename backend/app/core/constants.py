API_V1_STR = "/api/v1"
PROJECT_NAME = "Single Image 3D System"

# Pipeline stage names
STAGE_VALIDATION = "Validation"
STAGE_ANALYSIS = "Image Analysis"
STAGE_CLAHE = "CLAHE"
STAGE_FLORENCE_CAPTION = "Florence-2"
STAGE_GROUNDING_DINO = "GroundingDINO"
STAGE_FLORENCE_PARTS = "Part Detection"
STAGE_SAM = "SAM2.1"
STAGE_REMBG = "Background Removal"
STAGE_HUNYUAN_SHAPE = "3D Generation"
STAGE_HUNYUAN_TEXTURE = "Texture Generation"
STAGE_POINTCLOUD = "Point Cloud"
STAGE_DBSCAN = "Completed" # Final output state

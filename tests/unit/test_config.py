from backend.app.core.settings import settings
from backend.app.utils.logger import logger

def test_yaml_config_loading():
    # Verify values from configs/app.yaml
    assert settings.app.name == "Single Image 3D System"
    assert settings.app.version == "1.0.0"
    assert settings.app.max_upload_size_mb == 25
    
    # Verify values from configs/image_processing.yaml
    assert settings.image_processing.image.brightness_threshold == 0.30
    assert settings.image_processing.clahe.clip_limit == 2.0
    
    # Verify values from configs/grounding_dino.yaml
    assert settings.grounding_dino.thresholds.pass4 == 0.10
    
    # Verify values from configs/pointcloud.yaml
    assert settings.pointcloud.target_points == 100000

def test_logger_functionality():
    # Test logger does not throw exceptions
    logger.info("Test logger call from configuration unit test.")

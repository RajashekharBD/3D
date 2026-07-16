import os
import yaml
import logging

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Default log file path
log_file = "logs/pipeline.log"
log_level = "INFO"
console_output = True

# Try to load configs/logging.yaml
config_path = "configs/logging.yaml"
if os.path.exists(config_path):
    try:
        with open(config_path, "r") as f:
            log_config = yaml.safe_load(f)
            if log_config and "logging" in log_config:
                cfg = log_config["logging"]
                log_level = cfg.get("level", log_level)
                log_file = cfg.get("file", log_file)
                console_output = cfg.get("console", console_output)
    except Exception as e:
        print(f"Error loading logging config, using defaults. Exception: {e}")

# Map log level string to logging module level
numeric_level = getattr(logging, log_level.upper(), logging.INFO)

# Setup handlers
handlers = []
if log_file:
    # Ensure folder for log file exists
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    handlers.append(logging.FileHandler(log_file))

if console_output:
    handlers.append(logging.StreamHandler())

# Configure base logger
logging.basicConfig(
    level=numeric_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=handlers
)

logger = logging.getLogger("SingleImage3D")
logger.info(f"Logging initialized at level {log_level}. Log file: {log_file}")

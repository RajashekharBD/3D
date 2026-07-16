import os
import sys

def setup_directories():
    """Create all required project directories if they do not exist."""
    dirs = [
        "backend/app/api",
        "backend/app/controllers",
        "backend/app/services",
        "backend/app/pipeline",
        "backend/app/models",
        "backend/app/utils",
        "backend/app/schemas",
        "backend/app/middleware",
        "backend/app/core",
        "backend/app/config",
        "frontend/app",
        "frontend/components",
        "frontend/hooks",
        "frontend/services",
        "frontend/styles",
        "frontend/public",
        "frontend/types",
        "frontend/utils",
        "ai_models/florence2",
        "ai_models/grounding_dino",
        "ai_models/sam2",
        "ai_models/hunyuan3d",
        "ai_models/rembg",
        "ai_models/common",
        "configs",
        "data/input",
        "data/processed",
        "data/temp",
        "data/cache",
        "outputs/images",
        "outputs/meshes",
        "outputs/pointcloud",
        "outputs/metadata",
        "scripts",
        "tests/unit",
        "tests/integration",
        "tests/performance",
        "tests/fixtures",
        "logs",
        "docker"
    ]
    
    print("Setting up directory structure...")
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        # Create .gitkeep in folders that should not be empty
        if any(x in d for x in ["data/", "outputs/", "logs/"]):
            gitkeep_path = os.path.join(d, ".gitkeep")
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write("# Keep directory\n")
    print("Directory structure set up successfully.")

def check_python_version():
    """Verify python version is 3.11+."""
    version = sys.version_info
    print(f"Detected Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 11:
        print("Python version is compatible.")
        return True
    else:
        print("Warning: Python version 3.11+ is recommended.")
        return False

def check_cuda():
    """Check PyTorch and CUDA status if PyTorch is installed."""
    try:
        import torch
        print("PyTorch is installed.")
        cuda_avail = torch.cuda.is_available()
        print(f"CUDA Available: {cuda_avail}")
        if cuda_avail:
            print(f"CUDA Device Name: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("PyTorch not installed yet. Please run: pip install -r requirements.txt")

if __name__ == "__main__":
    setup_directories()
    check_python_version()
    check_cuda()

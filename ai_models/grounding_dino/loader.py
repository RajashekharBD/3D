import gc
import torch
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
from backend.app.core.settings import settings

MODEL_ID = "IDEA-Research/grounding-dino-tiny"

def load_grounding_dino_model():
    """Loads GroundingDINO model and processor."""
    device = settings.florence2.device  # Use configured device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(MODEL_ID).to(device)
    model.eval()

    return model, processor

def unload_grounding_dino_model(model):
    """Safely unloads the GroundingDINO model and clears CUDA cache."""
    if model is not None:
        try:
            model.to("cpu")
        except Exception:
            pass
        del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

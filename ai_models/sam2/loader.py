import gc
import torch
from transformers import AutoProcessor, Sam2Model
from backend.app.core.settings import settings

MODEL_ID = "facebook/sam2-hiera-tiny"

def load_sam2_model():
    """Loads facebook/sam2-hiera-tiny model and processor."""
    device = settings.sam2.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    # Select precision
    torch_dtype = torch.float16 if settings.florence2.precision == "float16" and device == "cuda" else torch.float32

    processor = AutoProcessor.from_pretrained(MODEL_ID)
    model = Sam2Model.from_pretrained(
        MODEL_ID,
        torch_dtype=torch_dtype
    ).to(device)
    model.eval()

    return model, processor

def unload_sam2_model(model):
    """Safely unloads the SAM 2 model and clears CUDA cache."""
    if model is not None:
        try:
            model.to("cpu")
        except Exception:
            pass
        del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

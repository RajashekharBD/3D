import gc
import torch
from transformers import AutoModelForCausalLM, AutoProcessor, AutoConfig
from backend.app.core.settings import settings
from backend.app.utils.logger import logger

MODEL_ID = "microsoft/Florence-2-base"

def load_florence2_model():
    """Loads Florence-2 model and processor based on configured device and precision."""
    device = settings.florence2.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    precision = settings.florence2.precision
    
    # Select torch dtype
    torch_dtype = torch.float16 if precision == "float16" and device == "cuda" else torch.float32

    # Patch dynamic module classes to avoid AttributeError: _supports_sdpa in newer transformers versions
    try:
        from transformers.dynamic_module_utils import get_class_from_dynamic_module
        model_cls = get_class_from_dynamic_module("modeling_florence2.Florence2ForConditionalGeneration", MODEL_ID)
        if model_cls is not None:
            model_cls._supports_sdpa = False
        pretrained_cls = get_class_from_dynamic_module("modeling_florence2.Florence2PreTrainedModel", MODEL_ID)
        if pretrained_cls is not None:
            pretrained_cls._supports_sdpa = False
    except Exception as e:
        logger.warning(f"Could not dynamically patch Florence-2 classes: {e}")

    # Load processor and model using the community workaround for the forced_bos_token_id bug
    processor = AutoProcessor.from_pretrained(MODEL_ID, trust_remote_code=True)
    
    config = AutoConfig.from_pretrained(
        MODEL_ID, 
        trust_remote_code=True,
        forced_bos_token_id=None
    )
    if hasattr(config, "text_config"):
        config.text_config.forced_bos_token_id = None

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        config=config,
        torch_dtype=torch_dtype,
        trust_remote_code=True
    ).to(device)
    
    # Set to evaluation mode
    model.eval()

    return model, processor

def unload_florence2_model(model):
    """Safely unloads the Florence-2 model and clears the CUDA cache to recover VRAM."""
    if model is not None:
        try:
            model.to("cpu")
        except Exception:
            pass
        del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

import torch
from PIL import Image
from backend.app.core.settings import settings

def generate_caption(image_path: str, model, processor) -> str:
    """Generates a caption for the given image path using Florence-2 VLM."""
    image = Image.open(image_path).convert("RGB")
    
    # Florence-2 task prompt for captioning
    prompt = "<CAPTION>"
    
    device = settings.florence2.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"
        
    precision = settings.florence2.precision
    torch_dtype = torch.float16 if precision == "float16" and device == "cuda" else torch.float32

    # Process inputs
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    
    # Cast pixel values to configured precision, move everything to device
    inputs = {
        k: v.to(device).to(torch_dtype) if (v.dtype == torch.float or v.dtype == torch.float32) else v.to(device)
        for k, v in inputs.items()
    }

    # Generate tokens
    beam_search = settings.florence2.beam_search
    max_tokens = settings.florence2.max_tokens
    temperature = settings.florence2.temperature

    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=max_tokens,
            do_sample=temperature > 0.0,
            temperature=temperature if temperature > 0.0 else 1.0,
            num_beams=3 if beam_search else 1,
            use_cache=False
        )

    # Decode output caption
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text.strip()

def transform_caption_to_prompt(caption: str) -> str:
    """Transforms a raw text caption into a GroundingDINO dot-separated prompt.
    
    Example: "a black ceramic mug" -> "black . ceramic . mug"
    """
    # Clean text and lower case
    words = caption.lower().strip().split()
    
    # Remove common filler stop-words
    stop_words = {"a", "an", "the", "of", "with", "on", "in", "at", "by", "for"}
    filtered_words = [w for w in words if w not in stop_words and len(w) > 0]
    
    # Join with dot separator
    return " . ".join(filtered_words)

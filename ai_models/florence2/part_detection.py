import torch
from PIL import Image
from backend.app.core.settings import settings

def detect_parts(image_path: str, parts_list: list, model, processor) -> dict:
    """Executes open vocabulary part detection using Florence-2 VLM on target parts.
    
    Returns a dictionary with part names as keys and list of bounding boxes [[xmin, ymin, xmax, ymax]] as values.
    """
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    # Join the requested parts by comma
    parts_query = ", ".join(parts_list)
    prompt = f"<OPEN_VOCABULARY_DETECTION>{parts_query}"

    device = settings.florence2.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    precision = settings.florence2.precision
    torch_dtype = torch.float16 if precision == "float16" and device == "cuda" else torch.float32

    # Process inputs
    inputs = processor(text=prompt, images=image, return_tensors="pt")
    
    # Cast pixel values and move to device
    inputs = {
        k: v.to(device).to(torch_dtype) if (v.dtype == torch.float or v.dtype == torch.float32) else v.to(device)
        for k, v in inputs.items()
    }

    # Generate
    beam_search = settings.florence2.beam_search
    max_tokens = settings.florence2.max_tokens
    
    with torch.no_grad():
        generated_ids = model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=max_tokens,
            num_beams=3 if beam_search else 1,
            use_cache=False
        )

    # Decode and parse
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    parsed_answer = processor.post_process_generation(
        generated_text,
        task="<OPEN_VOCABULARY_DETECTION>",
        image_size=(width, height)
    )

    # parsed_answer is usually: {"<OPEN_VOCABULARY_DETECTION>": {"bboxes": [[...]], "labels": [...]}}
    detection_data = parsed_answer.get("<OPEN_VOCABULARY_DETECTION>", {})
    bboxes = detection_data.get("bboxes", [])
    labels = detection_data.get("labels", [])

    # Group bboxes by label
    results = {}
    for box, label in zip(bboxes, labels):
        # Convert box coordinates to standard [xmin, ymin, xmax, ymax] integers
        xmin, ymin, xmax, ymax = box
        lbl = label.strip().lower()
        if lbl not in results:
            results[lbl] = []
        results[lbl].append([int(xmin), int(ymin), int(xmax), int(ymax)])

    return results

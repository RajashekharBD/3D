import torch
from PIL import Image
from backend.app.core.settings import settings

def detect_objects(image_path: str, text_prompt: str, threshold: float, model, processor) -> list:
    """Executes GroundingDINO object detection on the image using the given prompt and threshold.
    
    Returns a list of detected bounding boxes, where each box is [xmin, ymin, xmax, ymax] (pixel coords),
    sorted by descending confidence score.
    """
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    
    device = settings.florence2.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    # GroundingDINO requires trailing dot for prompt segments
    if not text_prompt.endswith("."):
        text_prompt = text_prompt + " ."

    # Preprocess inputs
    inputs = processor(images=image, text=text_prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    # Post process results
    results = processor.post_process_grounded_object_detection(
        outputs,
        inputs.input_ids,
        threshold=threshold,
        text_threshold=max(0.05, threshold - 0.05),
        target_sizes=[(height, width)]
    )[0]

    # Structure list of detected objects
    detections = []
    scores = results["scores"].cpu().tolist()
    boxes = results["boxes"].cpu().tolist()
    labels = results["labels"]

    for score, box, label in zip(scores, boxes, labels):
        # Coordinates in [xmin, ymin, xmax, ymax]
        xmin, ymin, xmax, ymax = box
        detections.append({
            "box": [int(xmin), int(ymin), int(xmax), int(ymax)],
            "score": float(score),
            "label": label
        })

    # Sort detections by score descending
    detections = sorted(detections, key=lambda x: x["score"], reverse=True)
    return detections

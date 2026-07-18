import torch
import numpy as np
from PIL import Image
from backend.app.core.settings import settings

def segment_image(image_path: str, bbox: list, model, processor) -> np.ndarray:
    """Executes SAM 2 segmentation on the image using the provided bounding box prompt.
    
    Returns a binary mask as a numpy array of shape (H, W) with values 0 (background) and 255 (foreground).
    """
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    device = settings.sam2.device
    if device == "cuda" and not torch.cuda.is_available():
        device = "cpu"

    precision = settings.florence2.precision
    torch_dtype = torch.float16 if precision == "float16" and device == "cuda" else torch.float32

    # SAM 2 expects: [batch_size, num_boxes, 4]
    input_boxes = [[bbox]]

    # Preprocess inputs
    inputs = processor(images=image, input_boxes=input_boxes, return_tensors="pt")
    
    # Extract dimensions before transferring to device (in case tensor migration alters the structure)
    original_sizes = inputs.get("original_sizes")
    reshaped_input_sizes = inputs.get("reshaped_input_sizes")

    # Transfer input tensors to the target device
    inputs = {
        k: v.to(device).to(torch_dtype) if (v.dtype == torch.float or v.dtype == torch.float32) else v.to(device)
        for k, v in inputs.items()
    }

    with torch.no_grad():
        outputs = model(**inputs)

    # Post process output masks
    masks = processor.post_process_masks(
        outputs.pred_masks,
        original_sizes
    )[0] # First batch element

    # If shape is (1, 3, H, W), squeeze
    if len(masks.shape) == 4:
        masks = masks[0]

    # Scores shape: (1, 1, 3)
    scores = outputs.iou_scores[0, 0].cpu().numpy() # shape (3,)

    # Find the mask index with the highest IoU score
    best_idx = int(np.argmax(scores))

    # Extract the best mask and convert from boolean tensor to uint8 numpy array
    best_mask = masks[best_idx].cpu().numpy()
    binary_mask = (best_mask * 255).astype(np.uint8)

    return binary_mask

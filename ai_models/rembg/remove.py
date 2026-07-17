import numpy as np
from PIL import Image
from rembg import remove, new_session
from backend.app.utils.logger import logger

def remove_background(image_path: str, mask_path: str) -> Image.Image:
    """Removes the background using rembg and applies the SAM 2 mask to refine the alpha channel.
    
    Returns a transparent PIL RGBA Image.
    """
    logger.info("Running rembg background removal...")
    orig_img = Image.open(image_path).convert("RGB")
    
    # Run rembg background removal
    session = new_session("u2net")
    rgba_img = remove(orig_img, session=session)
    
    # Load SAM 2 mask from Phase 12
    logger.info(f"Loading SAM 2 mask from: {mask_path}")
    mask_img = Image.open(mask_path).convert("L")
    mask_np = np.array(mask_img)
    
    # Apply SAM 2 mask to the alpha channel of the rembg output
    rgba_np = np.array(rgba_img)
    
    # Where SAM 2 mask is background (0), set alpha channel to 0
    rgba_np[mask_np == 0, 3] = 0
    
    final_rgba = Image.fromarray(rgba_np)
    return final_rgba

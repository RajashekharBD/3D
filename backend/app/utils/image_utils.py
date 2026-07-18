import cv2
import numpy as np

def analyze_image_properties(file_path: str) -> dict:
    """Calculates image properties: width, height, channels, mean brightness, and contrast.
    
    All brightness and contrast metrics are normalized between 0.0 and 1.0.
    """
    img = cv2.imread(file_path)
    if img is None:
        raise ValueError(f"Could not load image at path: {file_path}")

    height, width, channels = img.shape

    # Convert to grayscale to compute brightness and contrast standard deviation
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Normalized mean brightness (0.0 to 1.0)
    mean_brightness = float(np.mean(gray) / 255.0)
    
    # Normalized contrast (standard deviation of pixel values, 0.0 to 1.0)
    contrast = float(np.std(gray) / 255.0)

    return {
        "width": width,
        "height": height,
        "channels": channels,
        "mean_brightness": mean_brightness,
        "contrast": contrast
    }

def is_clahe_required(properties: dict, brightness_threshold: float = 0.30, contrast_threshold: float = 0.15) -> bool:
    """Decision logic to evaluate if the image is dark or low contrast."""
    is_dark = properties["mean_brightness"] < brightness_threshold
    is_low_contrast = properties["contrast"] < contrast_threshold
    return is_dark or is_low_contrast

def apply_clahe_to_image(file_path: str, dest_path: str, clip_limit: float = 2.0, tile_grid_size: int = 8) -> None:
    """Applies Contrast Limited Adaptive Histogram Equalization (CLAHE) on the L-channel of the image."""
    img = cv2.imread(file_path)
    if img is None:
        raise ValueError(f"Could not load image for CLAHE: {file_path}")

    # Convert to LAB space
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Instantiate CLAHE
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_grid_size, tile_grid_size))
    cl = clahe.apply(l)

    # Merge channels and convert back to BGR
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Save output
    cv2.imwrite(dest_path, enhanced_img)


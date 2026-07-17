import os
from PIL import Image
from backend.app.core.settings import settings
from backend.app.core.exceptions import (
    ImageValidationError,
    EmptyFile,
    InvalidImageFormat,
    InvalidMimeType,
    InvalidMagicBytes,
    CorruptedImage,
    InvalidImageDimensions
)

def validate_image_file_path(file_path: str) -> None:
    """Performs validation checks on a physical image file path."""
    # 1. File exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # 2. File is not empty
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise EmptyFile()

    # 3. File extension is allowed
    ext = file_path.split(".")[-1].lower() if "." in file_path else ""
    if ext not in settings.app.allowed_extensions:
        raise InvalidImageFormat(f"Extension '.{ext}' is not supported.")

    # Read binary header for magic bytes verification
    with open(file_path, "rb") as f:
        header = f.read(12)

    # 4 & 5. Validate file header magic bytes
    is_valid_header = False
    
    # JPEG magic bytes: FF D8 FF
    if ext in ["jpg", "jpeg"] and header.startswith(b"\xff\xd8\xff"):
        is_valid_header = True
    # PNG magic bytes: 89 50 4E 47 0D 0A 1A 0A
    elif ext == "png" and header.startswith(b"\x89PNG\r\n\x1a\n"):
        is_valid_header = True
    # WEBP magic bytes: RIFF (bytes 0-3) and WEBP (bytes 8-11)
    elif ext == "webp" and header.startswith(b"RIFF") and header[8:12] == b"WEBP":
        is_valid_header = True
    # BMP magic bytes: BM (bytes 0-1)
    elif ext == "bmp" and header.startswith(b"BM"):
        is_valid_header = True

    if not is_valid_header:
        raise InvalidMagicBytes()

    # 6. Validate image integrity using Pillow
    try:
        with Image.open(file_path) as img:
            img.verify()
    except Exception:
        raise CorruptedImage()

    # 7. Validate image dimensions
    try:
        # Re-open after verify() since verify() closes file handles or invalidates the image instance
        with Image.open(file_path) as img:
            width, height = img.size
            
            limits = settings.image_processing.image
            if width < limits.min_width or height < limits.min_height:
                raise InvalidImageDimensions(
                    f"Image size ({width}x{height}) is too small. Minimum required: {limits.min_width}x{limits.min_height}"
                )
            if width > limits.max_width or height > limits.max_height:
                raise InvalidImageDimensions(
                    f"Image size ({width}x{height}) exceeds maximum limit of {limits.max_width}x{limits.max_height}"
                )
    except ImageValidationError:
        raise
    except Exception:
        raise CorruptedImage()

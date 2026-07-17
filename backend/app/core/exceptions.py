from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    def __init__(self, status_code: int, message: str, stage: str = None):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.stage = stage

class ImageValidationError(BaseAppException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message, stage="Validation")

class PipelineError(BaseAppException):
    def __init__(self, message: str, stage: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message, stage=stage)

# Custom Validation Exceptions
class EmptyFile(ImageValidationError):
    def __init__(self, message: str = "Uploaded file is empty."):
        super().__init__(message)

class InvalidImageFormat(ImageValidationError):
    def __init__(self, message: str = "Unsupported or invalid image extension."):
        super().__init__(message)

class InvalidMimeType(ImageValidationError):
    def __init__(self, message: str = "MIME type is not allowed."):
        super().__init__(message)

class InvalidMagicBytes(ImageValidationError):
    def __init__(self, message: str = "File headers do not match allowed image magic bytes."):
        super().__init__(message)

class CorruptedImage(ImageValidationError):
    def __init__(self, message: str = "Image file is corrupted or unreadable."):
        super().__init__(message)

class ImageTooLarge(ImageValidationError):
    def __init__(self, message: str = "Image exceeds maximum allowed file size."):
        super().__init__(message)

class InvalidImageDimensions(ImageValidationError):
    def __init__(self, message: str = "Image dimensions are invalid."):
        super().__init__(message)

class NoObjectDetected(BaseAppException):
    def __init__(self, message: str = "No bounding box detected for the object in the image."):
        super().__init__(status_code=422, message=message, stage="Object Detection")


from fastapi import HTTPException, status

class BaseAppException(HTTPException):
    def __init__(self, status_code: int, message: str, stage: str = None):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.stage = stage

class ImageValidationError(BaseAppException):
    def __init__(self, message: str):
        super().__init__(status_code=status_code.HTTP_400_BAD_REQUEST, message=message, stage="Validation")

class PipelineError(BaseAppException):
    def __init__(self, message: str, stage: str):
        super().__init__(status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR, message=message, stage=stage)

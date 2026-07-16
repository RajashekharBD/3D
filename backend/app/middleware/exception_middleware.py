from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.core.exceptions import BaseAppException

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except BaseAppException as exc:
            content = {
                "success": False,
                "message": exc.message
            }
            if exc.stage:
                content["stage"] = exc.stage
            return JSONResponse(status_code=exc.status_code, content=content)
        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "message": f"An unexpected error occurred: {str(exc)}"
                }
            )

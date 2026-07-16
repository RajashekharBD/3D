import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.settings import settings
from backend.app.core.exceptions import BaseAppException
from backend.app.middleware.exception_middleware import ExceptionHandlingMiddleware
from backend.app.api.health import router as health_router
from backend.app.api.upload import router as upload_router

app = FastAPI(
    title=settings.APP_NAME,
    description="Automated Single-Image to 3D Asset System Backend API",
    version="1.0.0",
    docs_url="/docs" if settings.APP_ENV == "development" else None,
    redoc_url=None
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handling middleware
app.add_middleware(ExceptionHandlingMiddleware)

# Custom Exception Handler for BaseAppException
@app.exception_handler(BaseAppException)
async def app_exception_handler(request: Request, exc: BaseAppException):
    content = {
        "success": False,
        "message": exc.message
    }
    if exc.stage:
        content["stage"] = exc.stage
    return JSONResponse(status_code=exc.status_code, content=content)

# Routes
app.include_router(health_router, prefix="/api/v1")
app.include_router(upload_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host=settings.HOST, port=settings.PORT, reload=True)

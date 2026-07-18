from fastapi import APIRouter, Depends
from backend.app.core.auth import get_current_user
from backend.app.controllers.profile_controller import profile_controller

router = APIRouter()

@router.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    """Retrieves authenticated user profile information and usage statistics."""
    return profile_controller.get_profile(current_user)

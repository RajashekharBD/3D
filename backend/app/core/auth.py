import logging
import httpx
from fastapi import Security, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.settings import settings

logger = logging.getLogger("SingleImage3D")
security = HTTPBearer(auto_error=False)

def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """FastAPI dependency to extract and verify the Supabase JWT.
    
    Checks Authorization header first, then falls back to token query parameter.
    Verifies token directly against Supabase Auth API to handle ES256/HS256 algorithms seamlessly.
    """
    token = None
    if credentials:
        token = credentials.credentials
    if not token:
        token = request.query_params.get("token")

    if not token:
        if not settings.SUPABASE_JWT_SECRET:
            logger.warning("SUPABASE_JWT_SECRET not configured. Using Mock User fallback for local development.")
            return {
                "id": "d0000000-0000-0000-0000-000000000000",
                "email": "local_user@example.com"
            }
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated: Authorization token is missing."
        )

    # Perform direct token verification with Supabase Auth endpoint
    try:
        url = f"{settings.SUPABASE_URL}/auth/v1/user"
        headers = {
            "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {token}"
        }
        res = httpx.get(url, headers=headers, timeout=10.0)
        if res.status_code == 200:
            user_data = res.json()
            user_id = user_data.get("id")
            email = user_data.get("email")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials: user ID missing from auth provider response."
                )
                
            return {
                "id": user_id,
                "email": email
            }
        else:
            logger.error(f"Supabase auth check failed with status {res.status_code}: {res.text}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired authentication token."
            )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        logger.error(f"Supabase connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token verification failed."
        )

import logging
from supabase import create_client, Client
from backend.app.core.settings import settings

logger = logging.getLogger("SingleImage3D")

class Database:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_SERVICE_ROLE_KEY
        self.client = None
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
                logger.info("Supabase client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
        else:
            logger.warning("Supabase credentials not configured. Database features will operate in local/mock mode.")

    def get_client(self) -> Client:
        if not self.client:
            raise RuntimeError("Supabase client is not initialized. Please configure env variables.")
        return self.client

    @property
    def is_enabled(self) -> bool:
        return self.client is not None

db = Database()

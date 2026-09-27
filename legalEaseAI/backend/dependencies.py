# backend/dependencies.py
import os
from functools import lru_cache

class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    ENV: str = os.getenv("ENV", "development")

@lru_cache
def get_settings():
    return Settings()
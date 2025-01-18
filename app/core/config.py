from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import secrets
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    # Base
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Books API")
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "7"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///app/db/books.db")
    PORT: int = int(os.getenv("PORT", "8000"))

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
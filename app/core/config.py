from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings and configuration.
    Uses pydantic-settings to load from environment variables.
    """
    # Database
    DATABASE_URL: str = "sqlite:///./task_management.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS - will be parsed from comma-separated string in .env
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    # Application
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Task Management API"
    VERSION: str = "1.0.0"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS string into list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
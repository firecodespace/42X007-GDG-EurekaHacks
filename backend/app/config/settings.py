from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # API Keys
    gemini_api_key: str
    
    # Firebase
    firebase_project_id: str
    firebase_credentials_path: str = "secrets/gcp-sa.json"
    firestore_database: str = "(default)"
    
    # Logging
    log_level: str = "INFO"
    
    # HTTP Client
    max_concurrent_requests: int = 10
    request_timeout: int = 30
    
    # Retry Configuration
    retry_max_attempts: int = 3
    retry_backoff_factor: int = 2
    
    # Scheduler
    scheduler_enabled: bool = False
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"
    
    @property
    def firebase_credentials_full_path(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_dir, self.firebase_credentials_path)


settings = Settings()

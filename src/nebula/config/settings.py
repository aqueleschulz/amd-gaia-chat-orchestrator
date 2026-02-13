from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" 
    )
    app_name: str = "Nebula Orchestrator"
    app_env: str = "development"
    log_level: str = "INFO"
    
    lemonade_api_url: str = "http://localhost:8000/v1"
    
    model_name: str = "Gemma-3-4b-it-GGUF"
    workspace_dir: Path = Path("data")

settings = Settings()
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    app_name: str
    app_env: str = "development"
    log_level: str
    lemonade_api_url: str = "http://localhost:8000/v1"
    model_name: str = "deepseek-r1-distill-llama-8b"
    workspace_dir = (Path(__file__).parent / "data").resolve()

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings
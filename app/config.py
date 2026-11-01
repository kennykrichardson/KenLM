from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "KennyLM"
    app_version: str = "0.1.0"
    model_path: str = "/opt/kennylm/models/smollm2-135m-instruct-q4_k_m.gguf"
    model_repo: str = "tensorblock/SmolLM2-135M-Instruct-GGUF"
    model_filename: str = "SmolLM2-135M-Instruct-Q4_K_M.gguf"
    model_url: str = (
        "https://huggingface.co/tensorblock/SmolLM2-135M-Instruct-GGUF/"
        "resolve/main/SmolLM2-135M-Instruct-Q4_K_M.gguf"
    )
    context_size: int = 512
    max_tokens: int = 160
    temperature: float = 0.45
    api_key: str = Field(default="", validation_alias="KENNYLM_API_KEY")
    cors_origins: str = "*"
    model_threads: int = 1

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()

from pydantic import BaseModel, field_validator
from dotenv import load_dotenv
from pathlib import Path
import os

# Always load .env from project root
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class Settings(BaseModel):
    # ------------------------------------------------------------
    # LLM – Provider Selection
    # ------------------------------------------------------------
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    # allowed: "ollama", "openai"

    # ------------------------------------------------------------
    # Ollama
    # ------------------------------------------------------------
    ollama_base_url: str = os.getenv(
        "OLLAMA_BASE_URL", "http://localhost:11434"
    )
    ollama_model: str = os.getenv(
        "OLLAMA_MODEL", "llama3.1:latest"
    )

    # ------------------------------------------------------------
    # OpenAI
    # ------------------------------------------------------------
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv(
        "OPENAI_MODEL", "gpt-5-nano"
    )

    # ------------------------------------------------------------
    # APP
    # ------------------------------------------------------------
    env: str = os.getenv("ENV", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # ------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------
    @field_validator("llm_provider")
    @classmethod
    def validate_llm_provider(cls, v: str):
        allowed = {"ollama", "openai"}
        if v not in allowed:
            raise ValueError(
                f"Invalid LLM_PROVIDER '{v}'. Must be one of {allowed}"
            )
        return v

    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v, info):
        provider = info.data.get("llm_provider")
        if provider == "openai" and not v:
            raise ValueError(
                "OPENAI_API_KEY must be set when LLM_PROVIDER=openai"
            )
        return v


settings = Settings()

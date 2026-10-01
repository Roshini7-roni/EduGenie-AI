import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    # Keep the model configurable so the project can be updated without code changes.
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    explanation_provider: str = os.getenv("EXPLANATION_PROVIDER", "gemini").lower()
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M"
    )
    cors_origins: str = os.getenv("CORS_ORIGINS", "*")
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))
    debug: bool = _bool(os.getenv("DEBUG"), False)
    demo_mode: bool = _bool(os.getenv("DEMO_MODE"), False)


settings = Settings()
    
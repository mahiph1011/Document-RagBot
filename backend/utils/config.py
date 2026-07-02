from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Global application configuration.
    Values are loaded automatically from .env.
    """

    APP_NAME: str = "Enterprise RAG Chatbot"

    APP_VERSION: str = "1.0.0"

    GEMINI_API_KEY: str = ""

    DOCUMENT_PATH: str = "data/documents"

    UPLOAD_PATH: str = "data/uploads"

    VECTORSTORE_PATH: str = "data/vectorstore"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


BASE_DIR = Path(__file__).resolve().parent.parent
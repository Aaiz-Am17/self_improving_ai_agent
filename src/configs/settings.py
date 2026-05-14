"""
Centralized application settings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    # =====================================================
    # APPLICATION
    # =====================================================

    APP_NAME: str = "Industrial Agentic AutoML"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    # =====================================================
    # DATABASE
    # =====================================================

    SQLITE_DB_PATH: str = "checkpoints.db"

    FEEDBACK_DB_PATH: str = "feedback_logs.db"

    # =====================================================
    # EVALUATION
    # =====================================================

    EVALUATION_THRESHOLD: float = 0.70

    # =====================================================
    # VECTOR DATABASE
    # =====================================================

    CHROMA_DB_DIR: str = "chroma_db"

    # =====================================================
    # LOGGING
    # =====================================================

    LOG_DIR: str = "logs"

    REPORT_DIR: str = "reports"

    # =====================================================
    # API
    # =====================================================

    API_HOST: str = "0.0.0.0"

    API_PORT: int = 8000

    # =====================================================
    # ENV FILE
    # =====================================================

    class Config:

        env_file = ".env"


settings = Settings()
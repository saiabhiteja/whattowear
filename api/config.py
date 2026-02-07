"""
Application configuration using pydantic-settings.

Environment variables are loaded from .env file for local development
and from environment variables in production (Render free tier).
"""
import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central configuration class.
    All settings are loaded from environment variables
    to avoid hardcoding secrets or deployment-specific values.
    """

    database_url: str = "postgresql://localhost/wardrobe_ai"
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""

    # Application settings
    app_name: str = "Style Savvy"
    debug: bool = False

    class Config:
        # .env is optional (e.g. on Render, use Environment tab only)
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # ignore unknown env vars


def setup_logging() -> None:
    """
    Configure structured logging for the application.
    Using logging module instead of print() for production readiness
    and better control over log levels and formatting.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


settings = Settings()

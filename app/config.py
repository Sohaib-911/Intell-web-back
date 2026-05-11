"""
Application configuration via environment variables.
Uses Pydantic BaseSettings for type-safe config loading.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    # Email
    CONTACT_RECEIVER_EMAIL: str = os.getenv("CONTACT_RECEIVER_EMAIL")
    EMAIL_PROVIDER: Literal["smtp", "resend"] = os.getenv("EMAIL_PROVIDER")

    # SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = os.getenv("SMTP_PORT")
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")
    SMTP_FROM_NAME: str = "Intellisense Website"
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL")

    # Resend
    RESEND_API_KEY: str = ""

    # App
    FRONTEND_URL: str = "http://localhost:58193"
    ENVIRONMENT: Literal["development", "production"] = "development"


settings = Settings()

import os
from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    database_url: str = ""
    direct_url: str = ""
    supabase_url: str = Field(default="", alias="SUPABASE_URL")
    supabase_key: str = Field(default="", alias="SUPABASE_KEY")
    public_supabase_url: str = Field(default="", alias="PUBLIC_SUPABASE_URL")
    supabase_service_role_key: str = Field(
        default="", alias="SUPABASE_SERVICE_ROLE_KEY"
    )
    public_supabase_publishable_key: str = Field(
        default="", alias="PUBLIC_SUPABASE_PUBLISHABLE_KEY"
    )
    openai_api_key: str = ""
    google_cloud_services_api_key: str = Field(
        default="", alias="GOOGLE_CLOUD_SERVICES_API_KEY"
    )
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    scraper_service_url: str = Field(
        default="http://localhost:8081", alias="SCRAPER_SERVICE_URL"
    )
    api_base_url: str = Field(default="http://localhost:8000", alias="API_BASE_URL")
    scraper_callback_secret: str = Field(
        default="dev-secret", alias="SCRAPER_CALLBACK_SECRET"
    )
    environment: str = "development"
    log_level: str = "INFO"

    @model_validator(mode="after")
    def set_supabase_from_public_env(self):
        if not self.supabase_url and self.public_supabase_url:
            self.supabase_url = self.public_supabase_url
        if not self.supabase_key and self.public_supabase_publishable_key:
            self.supabase_key = self.public_supabase_publishable_key
        if not self.supabase_url:
            self.supabase_url = os.getenv("PUBLIC_SUPABASE_URL", "") or os.getenv(
                "SUPABASE_URL", ""
            )
        if not self.supabase_key:
            self.supabase_key = os.getenv(
                "PUBLIC_SUPABASE_PUBLISHABLE_KEY", ""
            ) or os.getenv("SUPABASE_KEY", "")
        return self

    @property
    def effective_database_url(self) -> str:
        return self.direct_url or self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()

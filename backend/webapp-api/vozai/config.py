import os
from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # Allow reading variables with different names
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
    gcp_project_id: str = Field(default="", alias="GCP_PROJECT_ID")
    gcp_location: str = Field(default="europe-central2", alias="GCP_LOCATION")
    cloud_tasks_queue: str = Field(
        default="campaign-generation-jobs", alias="CLOUD_TASKS_QUEUE"
    )
    worker_service_url: str = Field(default="", alias="WORKER_SERVICE_URL")
    worker_service_account_email: str = Field(
        default="", alias="WORKER_SERVICE_ACCOUNT_EMAIL"
    )
    scraper_service_url: str = Field(
        default="http://localhost:8081", alias="SCRAPER_SERVICE_URL"
    )
    environment: str = "development"
    log_level: str = "INFO"

    @model_validator(mode="after")
    def set_supabase_from_public_env(self):
        # Use PUBLIC_ prefixed vars as fallback if supabase_url/supabase_key are not set
        if not self.supabase_url and self.public_supabase_url:
            self.supabase_url = self.public_supabase_url
        if not self.supabase_key and self.public_supabase_publishable_key:
            self.supabase_key = self.public_supabase_publishable_key
        # Also check actual environment variables as final fallback
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

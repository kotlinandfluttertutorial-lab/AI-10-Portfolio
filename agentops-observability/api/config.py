"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str
    database_url_sync: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Security
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    # Application
    app_env: str = "development"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # Ingestion limits
    max_events_per_batch: int = 1000
    max_ingestion_payload_bytes: int = 10_485_760  # 10MB

    # Rate limiting
    rate_limit_ingestion_per_minute: int = 6000
    rate_limit_api_per_minute: int = 300

    @field_validator("jwt_secret")
    @classmethod
    def jwt_secret_must_not_be_placeholder(cls, v: str) -> str:
        if v.startswith("your-") or v == "changeme":
            raise ValueError(
                "JWT_SECRET must be set to a real secret, not a placeholder. "
                "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return v

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings. Fails fast on misconfiguration."""
    return Settings()  # type: ignore[call-arg]

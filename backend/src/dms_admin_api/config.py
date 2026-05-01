from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DMS Admin API"
    app_env: str = "development"
    admin_username: str = Field(default="admin")
    admin_password: str = Field(default="admin")
    session_secret: str = Field(default="change-me")
    dms_container_name: str = Field(default="mailserver")
    dms_config_dir: str = Field(default="/tmp/docker-mailserver")
    docker_binary: str = Field(default="docker")
    frontend_dist_dir: str = Field(default="/app/frontend-dist")

    model_config = SettingsConfigDict(
        env_prefix="DMS_ADMIN_",
        env_file=".env",
        extra="ignore",
    )

    @property
    def frontend_dist_path(self) -> Path:
        return Path(self.frontend_dist_dir)


@lru_cache
def get_settings() -> Settings:
    return Settings()

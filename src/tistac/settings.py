from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from tistac.constants import DEFAULT_LIMIT


class Settings(BaseSettings):
    """TiStac settings."""

    model_config = SettingsConfigDict(env_prefix="tistac_", env_file=".env")

    backend: str
    default_limit: int = Field(default=DEFAULT_LIMIT)
    catalog_id: str
    catalog_title: str | None = Field(default=None)
    catalog_description: str

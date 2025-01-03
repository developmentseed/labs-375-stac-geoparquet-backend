from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from tistac.constants import DEFAULT_LIMIT
from tistac.models.search import Search


class Settings(BaseSettings):
    """TiStac settings."""

    model_config = SettingsConfigDict(env_prefix="tistac_", env_file=".env")

    backend: str
    default_limit: int = Field(default=DEFAULT_LIMIT)
    catalog_id: str
    catalog_title: str | None = Field(default=None)
    catalog_description: str

    def update_search(self, search: Search) -> Search:
        """Updates a search with some default settings."""
        if search.limit is None:
            search.limit = self.default_limit
        return search

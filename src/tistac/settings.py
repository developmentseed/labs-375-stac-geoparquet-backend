from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .backend import Backend
from .constants import DEFAULT_LIMIT
from .search import Search


class Settings(BaseSettings):
    """TiStac settings."""

    model_config = SettingsConfigDict(env_prefix="tistac_")

    backend: str
    default_limit: int = Field(default=DEFAULT_LIMIT)

    def get_backend(self) -> Backend:
        """Returns the configured backend."""
        from .stac_geoparquet import StacGeoparquetBackend

        return StacGeoparquetBackend(self.backend)

    def update_search(self, search: Search) -> Search:
        """Updates a search with some default settings."""
        if search.limit is None:
            search.limit = self.default_limit
        return search

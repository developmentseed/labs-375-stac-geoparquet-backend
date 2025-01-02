import urllib.parse

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

    async def get_backend(self) -> Backend:
        """Returns the configured backend."""
        from .pgstac import PgstacBackend
        from .stac_geoparquet import StacGeoparquetBackend

        url = urllib.parse.urlparse(self.backend)
        if url.scheme == "postgresql":
            return await PgstacBackend.open(self.backend)
        else:
            return StacGeoparquetBackend(self.backend)

    def update_search(self, search: Search) -> Search:
        """Updates a search with some default settings."""
        if search.limit is None:
            search.limit = self.default_limit
        return search

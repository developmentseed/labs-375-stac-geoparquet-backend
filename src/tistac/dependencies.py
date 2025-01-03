import urllib.parse
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from tistac.backends import Backend
from tistac.backends.pgstac import PgstacBackend
from tistac.backends.stac_geoparquet import StacGeoparquetBackend
from tistac.settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


async def get_backend(settings: Annotated[Settings, Depends(get_settings)]) -> Backend:
    # TODO share the pgstac connection pool
    url = urllib.parse.urlparse(settings.backend)
    if url.scheme == "postgresql":
        return await PgstacBackend.open(settings.backend)
    else:
        return StacGeoparquetBackend(settings.backend)

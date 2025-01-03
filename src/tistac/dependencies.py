import urllib.parse
from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from tistac.backends import Backend
from tistac.backends.pgstac import PgstacBackend
from tistac.backends.stac_geoparquet import StacGeoparquetBackend
from tistac.settings import Settings

BACKEND: dict[str, Backend] = {}


@lru_cache
def get_settings() -> Settings:
    return Settings()


# I really don't like how this works -- we might want to go back to leaning on
# the starlette state, like stac-fastapi-pgstac does. It's just tricky to
# configure settings w/o using the dependency overrides.
async def get_backend(settings: Annotated[Settings, Depends(get_settings)]) -> Backend:
    global BACKEND

    url = urllib.parse.urlparse(settings.backend)
    if url.scheme == "postgresql":
        if "pgstac" in BACKEND:
            return BACKEND["pgstac"]
        else:
            BACKEND["pgstac"] = await PgstacBackend.open(settings.backend)
            return BACKEND["pgstac"]
    else:
        if "stac-geoparquet" in BACKEND:
            return BACKEND["stac-geoparquet"]
        else:
            BACKEND["stac-geoparquet"] = StacGeoparquetBackend(settings.backend)
            return BACKEND["stac-geoparquet"]

from stac_fastapi.types.config import ApiSettings


class Settings(ApiSettings):  # type: ignore
    """stac-fastapi-geoparquet settings"""

    stac_fastapi_geoparquet_href: str

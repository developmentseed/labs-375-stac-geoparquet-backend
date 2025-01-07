from stac_fastapi.types.config import ApiSettings


class Settings(ApiSettings):  # type: ignore
    """stac-fastapi-geoparquet settings"""

    href: str

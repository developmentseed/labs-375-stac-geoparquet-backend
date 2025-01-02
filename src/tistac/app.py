from typing import Annotated

from fastapi import Depends, FastAPI, Query

from .backend import Backend
from .item_collection import ItemCollection
from .root import Root
from .search import GetSearch, Search
from .settings import Settings


async def build(settings: Settings | None = None) -> FastAPI:
    """Builds a new TiStac application."""

    if settings is None:
        settings = Settings()  # type: ignore

    async def get_settings() -> Settings:
        return settings

    backend = await settings.get_backend()

    async def get_backend() -> Backend:
        return backend

    app = FastAPI()

    @app.get("/")
    async def root() -> Root:
        """The STAC API root."""

        return Root()

    @app.get("/search")
    async def get_search(
        get_search: Annotated[GetSearch, Query()],
        backend: Annotated[Backend, Depends(get_backend)],
        settings: Annotated[Settings, Depends(get_settings)],
    ) -> ItemCollection:
        """Searches this STAC API via a GET request."""
        search = get_search.into_search()
        search = settings.update_search(search)
        return await backend.search(search)

    @app.post("/search")
    async def post_search(
        search: Search,
        backend: Annotated[Backend, Depends(get_backend)],
        settings: Annotated[Settings, Depends(get_settings)],
    ) -> ItemCollection:
        """Searches this STAC API via a POST request."""
        search = settings.update_search(search)
        return await backend.search(search)

    return app

from fastapi import FastAPI

from .item_collection import ItemCollection
from .root import Root


def build() -> FastAPI:
    """Builds a new TiStac application."""

    app = FastAPI()

    @app.get("/")
    async def root() -> Root:
        """The STAC API root."""

        return Root()

    @app.get("/search")
    async def get_search() -> ItemCollection:
        """Searches this STAC API via a GET request."""

        return ItemCollection()

    @app.post("/search")
    async def post_search() -> ItemCollection:
        """Searches this STAC API via a POST request."""

        return ItemCollection()

    return app

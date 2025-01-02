from fastapi import FastAPI

from .root import Root


def build() -> FastAPI:
    """Builds a new TiStac application."""

    app = FastAPI()

    @app.get("/")
    async def root() -> Root:
        """The STAC API root."""

        return Root()

    return app

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from stacrs import DuckdbClient

from stac_fastapi.api.app import StacApi

from .client import Client
from .settings import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    client = DuckdbClient()
    collections = client.get_collections(settings.href)
    app.state.href = settings.href
    app.state.collections = collections
    app.state.client = client
    yield


api = StacApi(
    settings=Settings(
        stac_fastapi_landing_id="stac-fastapi-geoparquet",
        stac_fastapi_title="stac-geoparquet-geoparquet",
        stac_fastapi_description="A stac-fastapi server backend by stac-geoparquet",
    ),
    client=Client(),
    app=FastAPI(
        lifespan=lifespan,
        openapi_url=settings.openapi_url,
        docs_url=settings.docs_url,
        redoc_url=settings.docs_url,
    ),
)
app = api.app

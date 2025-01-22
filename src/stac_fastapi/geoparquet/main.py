from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, TypedDict

from fastapi import FastAPI
from stacrs import DuckdbClient

import stac_fastapi.api.models
from stac_fastapi.api.app import StacApi
from stac_fastapi.extensions.core.pagination import OffsetPaginationExtension

from .client import Client
from .search import SearchGetRequest, SearchPostRequest
from .settings import Settings

settings = Settings()


class State(TypedDict):
    """Application state."""

    client: DuckdbClient
    """The DuckDB client.
    
    It's just an in-memory DuckDB connection with the spatial extension enabled.
    """

    collections: dict[str, dict[str, Any]]
    """A mapping of collection id to collection."""

    hrefs: dict[str, str]
    """A mapping of collection id to geoparquet href."""


GetSearchRequestModel = stac_fastapi.api.models.create_request_model(
    model_name="SearchGetRequest",
    base_model=SearchGetRequest,
    mixins=[OffsetPaginationExtension().GET],
    request_type="GET",
)
PostSearchRequestModel = stac_fastapi.api.models.create_request_model(
    model_name="SearchPostRequest",
    base_model=SearchPostRequest,
    mixins=[OffsetPaginationExtension().POST],
    request_type="POST",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    client = DuckdbClient()
    collections = dict()
    hrefs = dict()
    for collection in client.get_collections(settings.stac_fastapi_geoparquet_href):
        if collection["id"] in collections:
            raise ValueError(
                "cannot have two items in the same collection in different geoparquet "
                "files"
            )
        else:
            collections[collection["id"]] = collection
        hrefs[collection["id"]] = settings.stac_fastapi_geoparquet_href
    yield {
        "client": client,
        "collections": collections,
        "hrefs": hrefs,
    }


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
    search_get_request_model=GetSearchRequestModel,
    search_post_request_model=PostSearchRequestModel,
)
app = api.app

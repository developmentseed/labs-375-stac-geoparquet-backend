from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from stacrs import DuckdbClient

import stac_fastapi.api.models
from stac_fastapi.api.app import StacApi
from stac_fastapi.extensions.core.pagination import OffsetPaginationExtension

from .client import Client
from .search import SearchGetRequest, SearchPostRequest
from .settings import Settings

settings = Settings()


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
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    client = DuckdbClient()
    collections = client.get_collections(settings.stac_fastapi_geoparquet_href)
    app.state.href = settings.stac_fastapi_geoparquet_href
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
    search_get_request_model=GetSearchRequestModel,
    search_post_request_model=PostSearchRequestModel,
)
app = api.app

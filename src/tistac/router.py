from typing import Annotated

from fastapi import APIRouter, Depends, Query

from tistac.backends import Backend
from tistac.dependencies import get_backend, get_settings
from tistac.models.item_collection import ItemCollection
from tistac.models.root import Root
from tistac.models.search import GetSearch, Search
from tistac.settings import Settings

router = APIRouter()


@router.get("/")
async def root() -> Root:
    """The STAC API root."""

    return Root()


@router.get("/search")
async def get_search(
    get_search: Annotated[GetSearch, Query()],
    backend: Annotated[Backend, Depends(get_backend)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ItemCollection:
    """Searches this STAC API via a GET request."""
    search = get_search.into_search()
    search = settings.update_search(search)
    return await backend.search(search)


@router.post("/search")
async def post_search(
    search: Search,
    backend: Annotated[Backend, Depends(get_backend)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ItemCollection:
    """Searches this STAC API via a POST request."""
    search = settings.update_search(search)
    return await backend.search(search)

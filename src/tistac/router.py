from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from tistac.backends import Backend
from tistac.dependencies import get_backend, get_settings
from tistac.models import Collection, GetSearch, ItemCollection, Link, Root, Search
from tistac.settings import Settings

router = APIRouter()


@router.get("/", tags=["root"], response_model_exclude_none=True)
async def root(
    backend: Annotated[Backend, Depends(get_backend)],
    settings: Annotated[Settings, Depends(get_settings)],
    request: Request,
) -> Root:
    """The STAC API root."""

    links = [
        Link(rel="self", href=str(request.url_for("root"))),
        Link(rel="root", href=str(request.url_for("root"))),
        Link(
            rel="service-desc",
            href=str(request.url_for("root")) + "openapi.json",
            type="application/vnd.oai.openapi+json;version=3.1",
        ),
        Link(
            rel="service-doc",
            href=str(request.url_for("root")) + "docs",
            type="text/html",
        ),
        Link(
            rel="search",
            href=str(request.url_for("get_search")),
            type="application/geo+json",
            method="GET",
        ),
        Link(
            rel="search",
            href=str(request.url_for("post_search")),
            type="application/geo+json",
            method="POST",
        ),
    ]

    for collection in await backend.get_collections():
        links.append(
            Link(
                rel="child",
                href=str(
                    request.url_for("get_collection", collection_id=collection.id)
                ),
            )
        )

    return Root(
        id=settings.catalog_id,
        title=settings.catalog_title,
        description=settings.catalog_description,
        links=links,
        conformsTo=[
            "https://api.stacspec.org/v1.0.0/core",
            "https://api.stacspec.org/v1.0.0/item-search",
        ],
    )


@router.get("/collections/{collection_id}", tags=["collections"])
async def get_collection(
    collection_id: str,
    backend: Annotated[Backend, Depends(get_backend)],
) -> Collection:
    if collection := await backend.get_collection(collection_id):
        return collection
    else:
        raise HTTPException(
            status_code=404, detail=f"Collection with id={collection_id} not found"
        )


@router.get("/search", tags=["search"], response_model_exclude_none=True)
async def get_search(
    get_search: Annotated[GetSearch, Query()],
    backend: Annotated[Backend, Depends(get_backend)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ItemCollection:
    """Searches this STAC API via a GET request."""
    search = get_search.into_search()
    search = search.with_settings(settings)
    return await backend.search(search)


@router.post("/search", tags=["search"], response_model_exclude_none=True)
async def post_search(
    search: Search,
    backend: Annotated[Backend, Depends(get_backend)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ItemCollection:
    """Searches this STAC API via a POST request."""
    search = search.with_settings(settings)
    return await backend.search(search)

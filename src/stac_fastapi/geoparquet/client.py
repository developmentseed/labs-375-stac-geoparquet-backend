from typing import Any

from geojson_pydantic.geometries import Geometry
from starlette.requests import Request

from stac_fastapi.types.core import AsyncBaseCoreClient
from stac_fastapi.types.errors import NotFoundError
from stac_fastapi.types.rfc3339 import DateTimeType
from stac_fastapi.types.search import BaseSearchPostRequest
from stac_fastapi.types.stac import BBox, Collection, Collections, Item, ItemCollection


class Client(AsyncBaseCoreClient):  # type: ignore
    """A stac-fastapi-geoparquet client."""

    async def all_collections(self, *, request: Request, **kwargs: Any) -> Collections:
        return Collections(collections=request.app.state.collections)

    async def get_collection(
        self, *, request: Request, collection_id: str, **kwargs: Any
    ) -> Collection:
        if collection := next(
            (c for c in request.app.state.collections if c["id"] == collection_id), None
        ):
            return Collection(**collection)
        else:
            raise NotFoundError(f"Collection does not exist: {collection_id}")

    async def get_item(
        self, *, request: Request, item_id: str, collection_id: str, **kwargs: Any
    ) -> Item:
        item_collection = request.app.state.client.search(
            request.app.state.href, ids=[item_id], collections=[collection_id]
        )
        if len(item_collection["features"]) == 1:
            return Item(**item_collection["features"][0])
        else:
            raise NotFoundError(
                f"Item does not exist: {item_id} in collection {collection_id}"
            )

    async def get_search(
        self,
        *,
        request: Request,
        collections: list[str] | None = None,
        ids: list[str] | None = None,
        bbox: BBox | None = None,
        intersects: Geometry | None = None,
        datetime: DateTimeType | None = None,
        limit: int | None = 10,
        **kwargs: Any,
    ) -> ItemCollection:
        search_request = BaseSearchPostRequest(
            collections=collections,
            ids=ids,
            bbox=bbox,
            intersects=intersects,
            datetime=datetime,
            limit=limit,
        )
        self.search(
            self,
            search_request=search_request,
            request=request,
            **kwargs,
        )

    async def item_collection(
        self,
        *,
        request: Request,
        bbox: BBox | None = None,
        datetime: DateTimeType | None = None,
        limit: int = 10,
        offset: int = 0,
        **kwargs: Any,
    ) -> ItemCollection:
        search_request = BaseSearchPostRequest(
            bbox=bbox, datetime=datetime, limit=limit, offset=offset
        )
        return self.search(search_request=search_request, request=request, **kwargs)

    async def post_search(
        self, search_request: BaseSearchPostRequest, *, request: Request, **kwargs: Any
    ) -> ItemCollection:
        return await self.search(
            search_request=search_request, request=request, **kwargs
        )

    async def search(
        self, *, search_request: BaseSearchPostRequest, request: Request, **kwargs
    ) -> ItemCollection:
        search = search_request.model_dump()
        search.update(**kwargs)
        item_collection = request.app.state.client.search(
            request.app.state.href,
            **search,
        )
        return ItemCollection(**item_collection)

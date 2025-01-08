import copy
import urllib.parse
from typing import Any

from geojson_pydantic.geometries import Geometry
from starlette.requests import Request

from stac_fastapi.api.models import BaseSearchPostRequest
from stac_fastapi.types.core import AsyncBaseCoreClient
from stac_fastapi.types.errors import NotFoundError
from stac_fastapi.types.rfc3339 import DateTimeType
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
            request.app.state.href, ids=[item_id], collections=[collection_id], **kwargs
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
        offset: int | None = 0,
        **kwargs,
    ) -> ItemCollection:
        search = BaseSearchPostRequest(
            collections=collections,
            ids=ids,
            bbox=bbox,
            intersects=intersects,
            datetime=datetime,
            limit=limit,
        )
        return await self.search(
            request=request, search=search, offset=offset, **kwargs
        )

    async def item_collection(
        self,
        *,
        request: Request,
        bbox: BBox | None = None,
        datetime: DateTimeType | None = None,
        limit: int = 10,
        offset: int = 0,
        **kwargs,
    ) -> ItemCollection:
        search = BaseSearchPostRequest(
            bbox=bbox, datetime=datetime, limit=limit, offset=offset
        )
        return await self.search(request=request, search=search, **kwargs)

    async def post_search(
        self, search_request: BaseSearchPostRequest, *, request: Request, **kwargs
    ) -> ItemCollection:
        return await self.search(search=search_request, request=request, **kwargs)

    async def search(
        self,
        *,
        request: Request,
        search: BaseSearchPostRequest,
        **kwargs,
    ) -> ItemCollection:
        search_dict = search.model_dump(exclude_none=True)
        search_dict.update(**kwargs)
        item_collection = request.app.state.client.search(
            request.app.state.href,
            **search_dict,
        )
        num_items = len(item_collection["features"])
        offset = int(search_dict.get("offset", None) or 0)

        try:
            limit = int(search_dict["limit"])
            if limit > num_items:
                limit = None
        except KeyError:
            limit = len(num_items)

        if limit:
            next_search = copy.deepcopy(search_dict)
            next_search["limit"] = limit
            next_search["offset"] = offset + limit
        else:
            next_search = None

        links = []
        url = request.url_for("Search")
        if next_search:
            if request.method == "GET":
                links.append(
                    {
                        "href": str(url) + "?" + urllib.parse.urlencode(next_search),
                        "rel": "next",
                        "type": "application/geo+json",
                        "method": "GET",
                    }
                )
            else:
                links.append(
                    {
                        "href": str(url),
                        "rel": "next",
                        "type": "application/geo+json",
                        "method": "POST",
                        "body": next_search,
                    }
                )

        item_collection["links"] = links
        return ItemCollection(**item_collection)

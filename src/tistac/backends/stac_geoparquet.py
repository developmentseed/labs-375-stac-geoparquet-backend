import stacrs
from pystac import Collection as PystacCollection
from pystac import Extent, Item
from stacrs import DuckdbClient

from tistac.backends import Backend
from tistac.models import Collection, ItemCollection, Link, Search


class StacGeoparquetBackend(Backend):
    """A stac-geoparquet backend, using DuckDB under the hood."""

    def __init__(self, href: str, base_url: str):
        # TODO support multiple collections
        # TODO store collection information in the **stac-geoparquet**
        items_as_dicts = stacrs.search(href)
        collection_ids = set()
        items = list()
        for item_as_dict in items_as_dicts:
            item = Item.from_dict(item_as_dict)
            if item.collection_id:
                collection_ids.add(item.collection_id)
            items.append(item)
        if len(collection_ids) != 1:
            raise Exception(
                "Only one collection id is supported by the "
                f"stac-geoparquet backend: {collection_ids}"
            )
        extent = Extent.from_items(items)
        collection = PystacCollection(
            id=collection_ids.pop(),
            description="An auto-generated stac-geoparquet Collection",
            extent=extent,
        )
        d = collection.to_dict(include_self_link=False, transform_hrefs=False)
        d["stac_version"] = "1.1.0"
        self.collections = [Collection.model_validate(d)]
        self.href = href
        self.base_url = base_url
        self.client = DuckdbClient()

    async def get_collections(self) -> list[Collection]:
        return self.collections

    async def get_collection(self, collection_id: str) -> Collection | None:
        return next((c for c in self.collections if c.id == collection_id), None)

    async def search(self, search: Search) -> ItemCollection:
        item_collection = self.client.search(self.href, **search.model_dump())
        number_returned = len(item_collection["features"])
        assert search.limit, "Search should always have a limit at this point"
        links = []
        if number_returned >= search.limit:
            links.append(
                self.next_link(
                    search.limit,
                    search.offset or 0,
                    number_returned,
                )
            )
        item_collection["numberReturned"] = number_returned
        item_collection["links"] = links
        return ItemCollection.model_validate(item_collection)

    def next_link(self, limit: int, offset: int, num_items: int) -> Link:
        # TODO support POST
        return Link(
            rel="next",
            type="application/geo+json",
            href=self.base_url + f"search?limit={limit}&offset={offset + num_items}",
            method="GET",
        )

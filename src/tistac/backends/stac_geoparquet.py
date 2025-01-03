import stacrs
from pystac import Collection as PystacCollection
from pystac import Extent, Item

from tistac.backends import Backend
from tistac.models import Collection, ItemCollection, Search


class StacGeoparquetBackend(Backend):
    """A stac-geoparquet backend, using DuckDB under the hood."""

    def __init__(self, href: str):
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

    async def get_collections(self) -> list[Collection]:
        return self.collections

    async def get_collection(self, collection_id: str) -> Collection | None:
        return next((c for c in self.collections if c.id == collection_id), None)

    async def search(self, search: Search) -> ItemCollection:
        items = stacrs.search(self.href, limit=search.limit)
        return ItemCollection(features=items)

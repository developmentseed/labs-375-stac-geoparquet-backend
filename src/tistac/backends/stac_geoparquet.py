import stacrs

from tistac.backends import Backend
from tistac.models.item_collection import ItemCollection
from tistac.models.search import Search


class StacGeoparquetBackend(Backend):
    """A stac-geoparquet backend, using DuckDB under the hood."""

    def __init__(self, href: str):
        self.href = href

    async def search(self, search: Search) -> ItemCollection:
        items = stacrs.search(self.href, limit=search.limit)
        return ItemCollection(features=items)

from __future__ import annotations

from pgstacrs import Client

from .backend import Backend
from .item_collection import ItemCollection
from .search import Search


class PgstacBackend(Backend):
    """A PgSTAC backend."""

    @classmethod
    async def open(cls, dsn: str) -> PgstacBackend:
        client = await Client.open(dsn)
        return PgstacBackend(client)

    def __init__(self, client: Client) -> None:
        self.client = client

    async def search(self, search: Search) -> ItemCollection:
        item_collection = await self.client.search(limit=search.limit)
        return ItemCollection.model_validate(item_collection)

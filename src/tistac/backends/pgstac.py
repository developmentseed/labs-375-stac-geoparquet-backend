from __future__ import annotations

from pgstacrs import Client

from tistac.backends import Backend
from tistac.models import Collection, ItemCollection, Search


class PgstacBackend(Backend):
    """A PgSTAC backend."""

    @classmethod
    async def open(cls, dsn: str, base_url: str) -> PgstacBackend:
        client = await Client.open(dsn)
        await client.set_setting("base_url", base_url)
        return PgstacBackend(client)

    def __init__(self, client: Client) -> None:
        self.client = client

    async def get_collections(self) -> list[Collection]:
        return [
            Collection.model_validate(d) for d in await self.client.all_collections()
        ]

    async def get_collection(self, collection_id: str) -> Collection | None:
        if d := await self.client.get_collection(collection_id):
            return Collection.model_validate(d)
        else:
            return None

    async def search(self, search: Search) -> ItemCollection:
        item_collection = await self.client.search(**search.model_dump())
        return ItemCollection.model_validate(item_collection)

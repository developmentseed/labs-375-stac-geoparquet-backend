from abc import ABC, abstractmethod

from tistac.models import Collection, ItemCollection, Search


class Backend(ABC):
    """A TiStac backend."""

    @abstractmethod
    async def get_collections(self) -> list[Collection]:
        """Returns all collections in this backend."""

    @abstractmethod
    async def get_collection(self, collection_id: str) -> Collection | None:
        """Returns a collection."""

    @abstractmethod
    async def search(self, search: Search) -> ItemCollection:
        """Searches this backend."""

from abc import ABC, abstractmethod

from .item_collection import ItemCollection
from .search import Search


class Backend(ABC):
    """A TiStac backend."""

    @abstractmethod
    async def search(self, search: Search) -> ItemCollection:
        """Searches this backend."""

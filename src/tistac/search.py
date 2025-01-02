from pydantic import BaseModel, Field


class Search(BaseModel):
    """A STAC API POST search."""

    limit: int | None = Field(default=None)
    """The maximum number of items per page."""


class GetSearch(BaseModel):
    """A STAC API GET search."""

    def into_search(self) -> Search:
        """Converts this GET search into a POST search."""
        return Search()

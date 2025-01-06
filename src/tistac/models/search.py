from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from tistac import Settings


class Search(BaseModel):
    """A STAC API POST search."""

    model_config = ConfigDict(extra="allow")

    limit: int | None = Field(default=None)
    offset: int | None = Field(default=None)

    def with_settings(self, settings: Settings) -> Search:
        if self.limit is None:
            self.limit = settings.default_limit
        return self


class GetSearch(BaseModel):
    """A STAC API GET search."""

    model_config = ConfigDict(extra="allow")

    def into_search(self) -> Search:
        """Converts this GET search into a POST search."""
        return Search(**self.model_dump())

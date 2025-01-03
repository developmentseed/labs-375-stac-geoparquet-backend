from typing import Any

from pydantic import BaseModel


class ItemCollection(BaseModel):
    """A STAC API item collection.

    The features of this collection may not be valid STAC items, if the `fields`
    extension is used.
    """

    features: list[dict[str, Any]]

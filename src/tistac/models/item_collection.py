from typing import Any, Literal

from pydantic import BaseModel, Field

from tistac.models.link import Link


class ItemCollection(BaseModel):
    """A STAC API item collection.

    The features of this collection may not be valid STAC items, if the `fields`
    extension is used.
    """

    type: Literal["FeatureCollection"] = Field(default="FeatureCollection")
    links: list[Link]
    number_returned: int = Field(alias="numberReturned")
    features: list[dict[str, Any]]

from typing import Literal

from pydantic import BaseModel, Field

from tistac.models import Link


class Root(BaseModel):
    """The root landing page of a STAC API."""

    type: Literal["Catalog"] = Field(default="Catalog")
    stac_version: str = Field(default="1.1.0")
    stac_extensions: list[str] = Field(default_factory=list)
    id: str
    title: str | None = Field(default=None)
    description: str
    conforms_to: list[str] = Field(alias="conformsTo")
    links: list[Link] = Field(default_factory=list)

from pydantic import BaseModel, ConfigDict


class Collection(BaseModel):
    """A STAC Collection"""

    model_config = ConfigDict(extra="allow")

    id: str

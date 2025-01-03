from pydantic import BaseModel, Field


class Link(BaseModel):
    rel: str
    type: str = Field("application/json")
    href: str
    method: str | None = Field(default=None)

from pydantic import BaseModel


class Page(BaseModel):
    """A page of a search response.

    Not exactly an item collection, but close.
    """

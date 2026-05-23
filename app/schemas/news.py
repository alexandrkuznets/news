from datetime import date
from pydantic import BaseModel


class NewsBase(BaseModel):
    title: str
    content: str
    source: str
    url: str
    published_at: date


class NewsCreate(NewsBase):
    pass


class NewsResponse(NewsBase):
    id: int

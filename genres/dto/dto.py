from typing import Annotated

from pydantic import BaseModel, Field


class GenreFields(BaseModel):
    slug: str | None = None
    description: str | None = None
    parent_id: str | None = None
    color: str | None = None
    icon: str | None = None
    name: str | None = None


class Genre(GenreFields):
    id: str
    name: str


class GenreCreate(GenreFields):
    name: Annotated[str, Field(min_length=1)]


class GenreUpdate(GenreFields):
    name: Annotated[str | None, Field(default=None, min_length=1)]

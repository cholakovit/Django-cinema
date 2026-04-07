from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1, max_length=512)
    year: int | None = Field(None, ge=0, le=10_000)
    description: str | None = None
    rating: float | None = Field(None, ge=0, le=10)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(MovieBase):
    name: str | None = Field(default=None, min_length=1, max_length=512)


class MovieResponse(MovieBase):
    id: str
    type: str = "movie"
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

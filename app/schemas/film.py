from pydantic import BaseModel, validator

from app.core.config import GENRES

class FilmBase(BaseModel):
    name_film: str | None = None
    genres: list[str] | None= None
    rating: int | None = None

class FilmGenres(FilmBase):
    @validator("genres")
    def genres_validate(cls, genres):
        if genres in GENRES:
            print(genres in GENRES)
            print(genres not in GENRES)
            raise ValueError("The specified genres are missing in the search")
        return genres
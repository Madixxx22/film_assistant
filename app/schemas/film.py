from pydantic import BaseModel, validator

from app.core.config import GENRES

class FilmBase(BaseModel):
    name_film: str = ""
    genres: list[str] = [""]


class Film(FilmBase):
    rating: float | None = None

class FilmFull(FilmBase):
    rating_start: float = 0
    rating_end: float = 10

class FilmGenres(BaseModel):
    genres: list[str]
    @validator("genres")
    def genres_validate(cls, genres):
        for i in genres:
            if i.lower() not in GENRES:
                raise ValueError("The specified genres are missing in the search")
            
        return genres

class FilmName(BaseModel):
    name_film: str
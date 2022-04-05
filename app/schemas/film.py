from pydantic import BaseModel, validator

from app.core.config import GENRES

class FilmBase(BaseModel):
    name_film: str | None = ""
    genres: list[str] | None= [""]
    rating: float | None = None

class Film(FilmBase):
    pass

class FilmGenres(BaseModel):
    genres: list[str]
    @validator("genres")
    def genres_validate(cls, genres):
        for i in genres:
            if i.lower() not in GENRES:
                raise ValueError("The specified genres are missing in the search")
            
        return genres

class FilmRating(BaseModel):
    rating_start: float
    rating_end: float
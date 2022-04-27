from pydantic import BaseModel, validator

from app.core.config import GENRES

class FilmBase(BaseModel):
    name_film: str = ""
    genres: list[str] = [""]
    #Checking for the correctness of genres
    @validator("genres")
    def genres_validate(cls, genres):
        for i in genres:
            if i.lower() not in GENRES:
                raise ValueError("The specified genres are missing in the search")
            elif genres == []:
                return genres 
        return genres

class Film(FilmBase):
    rating: float | None = None
    img_link: str | None = None

class FilmSearch(FilmBase):
    rating_start: float = 0
    rating_end: float = 10

class FilmHistory(Film):
    id_search_film: int
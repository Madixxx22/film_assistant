from fastapi import APIRouter

from app.schemas.film import FilmGenres, Film, FilmRating
from app.utils.film import search_film

router = APIRouter()

@router.post("/film_search_genres")
async def search_film_genres(film_genres: FilmGenres):
    return await search_film(Film(genres = film_genres.genres))


@router.post("/film_search_rating")
async def search_film_rating(film_genres: FilmRating):
    return await search_film(Film(genres = film_genres.genres))
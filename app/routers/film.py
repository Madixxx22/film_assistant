from fastapi import APIRouter

from app.schemas.film import FilmFull, FilmGenres, Film, FilmName
from app.utils.film import search_film

router = APIRouter()

@router.post("/film_search_genres")
async def search_film_genres(film_genres: FilmGenres):
    return await search_film(FilmFull(genres = film_genres.genres))


@router.post("/film_search_name")
async def search_film_name(film_name: FilmName):
    return await search_film(FilmFull(name_film = film_name.name_film))

@router.post("/film_search_full")
async def search_film_full(film_info: FilmFull):
    return await search_film(film_info)
from fastapi import APIRouter

from app.schemas.film import FilmGenres

router = APIRouter()

@router.post("/film_search_genres")
async def search_film_genres(film_req: FilmGenres):
    return film_req
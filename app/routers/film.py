from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.db.crud_film import film_crud
from app.db.crud_user import user_crud

from app.schemas.film import FilmFull, FilmGenres, FilmName
from app.core.config import templates
from app.schemas.user import User
from app.utils.film import search_film
from app.utils.users import get_current_active_user

router = APIRouter()

@router.post("/film-search-genres")
async def search_film_genres(film_genres: FilmGenres):
    return await search_film(FilmFull(genres = film_genres.genres))


@router.post("/film-search-name")
async def search_film_name(film_name: FilmName):
    return await search_film(FilmFull(name_film = film_name.name_film))

@router.post("/film-search-full")
async def search_film_full(film_info: FilmFull, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")
    await film_crud.create_search_film(film_info, current_user)
    return await search_film(film_info)

@router.get("/search-film-history")
async def search_film_history(current_user: User = Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")
    return await film_crud.get_history_search(current_user)
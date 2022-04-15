from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from app.db.crud_film import film_crud
from app.db.crud_user import user_crud
from app.schemas import film

from app.schemas.film import Film, FilmFull, FilmGenres, FilmName
from app.core.config import templates
from app.schemas.user import User
from app.utils.film import recommend, search_film
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

    id_search = await film_crud.get_id_search_film(current_user)
    films_response = await search_film(film_info)
    
    await film_crud.create_film_history_by_search(id_search["id_search"], films_response)
 
    return films_response

@router.get("/history-search")
async def search_film_history(current_user: User = Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")
    return await film_crud.get_history_search(current_user)


@router.get("/history-search/film-history-by-search")
async def film_history_by_search(id_search : int, current_user: User = Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")
    return await film_crud.get_history_film_by_search(id_search)

@router.delete("/clear_history_search")
async def clear_history_search(current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")
    
    return await film_crud.delete_history_search(current_user.login)

@router.post("/add_film_selected")
async def add_film_selected(film_select: Film, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="profile is not active")
    return await film_crud.create_film_selected(login = current_user.login, film = film_select)

@router.get("/selected_films")
async def view_selected_films(current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    return await film_crud.get_selected_films(current_user.login)

@router.delete("/delete_selected_films")
async def delete_selected_film(id_film: int, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    return await film_crud.delete_selected_film(id_film = id_film, login = current_user.login)

@router.get("/recommendations")
async def recommendations(count_genres: int, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")
    
    return await recommend(count_genres, current_user.login)
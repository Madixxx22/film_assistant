from fastapi import APIRouter, Depends, HTTPException, status

from backend.app.schemas.user import User
from backend.app.db.crud_film import film_crud
from backend.app.db.crud_user import user_crud
from backend.app.schemas.film import Film, FilmFull, FilmHistory
from backend.app.utils.film import recommend, search_film
from backend.app.utils.users import get_current_active_user

router = APIRouter(tags=["film"])

@router.post("/add-film-selected", status_code = status.HTTP_201_CREATED)
async def add_film_selected(film_select: Film, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code=400, detail="profile is not active")

    return await film_crud.create_film_selected(login = current_user.login, film = film_select)


@router.post("/film-search-full", response_model = list[Film], status_code = status.HTTP_200_OK)
async def search_film_full(film_info: FilmFull, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    await film_crud.create_search_film(film_info, current_user)

    id_search = await film_crud.get_id_search_film(current_user)
    films_response = await search_film(film_info)

    await film_crud.create_film_history_by_search(id_search["id_search"], films_response)
    return films_response

@router.get("/history-search", response_model = list[FilmFull], status_code = status.HTTP_200_OK)
async def search_film_history(current_user: User = Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    return await film_crud.get_history_search(current_user)

@router.get("/history-search/film-history-by-search", response_model = list[FilmHistory], status_code = status.HTTP_200_OK)
async def film_history_by_search(id_search: int, current_user: User = Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    return await film_crud.get_history_film_by_search(id_search)

@router.get("/selected-films", response_model = list[Film], status_code = status.HTTP_200_OK)
async def view_selected_films(current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    return await film_crud.get_selected_films(current_user.login)

@router.get("/recommendations", response_model = list[Film], status_code = status.HTTP_200_OK)
async def recommendations(count_genres: int, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    return await recommend(count_genres, current_user.login)

@router.delete("/clear-history-search", status_code = status.HTTP_200_OK)
async def clear_history_search(current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")

    return await film_crud.delete_history_search(current_user.login)

@router.delete("/delete-selected-films", status_code = status.HTTP_200_OK)
async def delete_selected_film(id_film: int, current_user: User =  Depends(get_current_active_user)):
    if not await user_crud.is_active(current_user):
        raise HTTPException(status_code = 400, detail="profile is not active")
        
    return await film_crud.delete_selected_film(id_film = id_film, login = current_user.login)
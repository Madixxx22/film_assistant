from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.schemas.user import User
from app.db.crud_film import film_crud
from app.db.crud_user import user_crud
from app.utils.film import recommend, search_film
from app.utils.users import get_current_active_user
from app.core.data_for_openapi import ExampleSchemes
from app.schemas.film import Film, FilmSearch, FilmHistory

router = APIRouter(tags=["film"])

@router.post("/add-film-selected", status_code = status.HTTP_201_CREATED)
async def add_film_selected(film_select: Film = Body(..., example = ExampleSchemes.film), current_user: User =  Depends(get_current_active_user)):
    """ 
    Add a film to your favorites(Authorized user only): 

    - **name_film**: The name of the film 
    - **genres**: List of film genres 
    - **rating**: Rating of the film on IMDB 
    - **img_link**: link to the movie poster from IMDB 

    Returns the id of the added film in the database
    """
    
    return await film_crud.create_film_selected(login = current_user.login, film = film_select)


@router.post("/film-search", response_model = list[Film], status_code = status.HTTP_200_OK, responses =  {200: { 
 "description": "Item requested by ID", 
 "content": { 
 "application/json": { 
 "example": ExampleSchemes.film_response 
 }}}})
async def film_search(film_info: FilmSearch = Body(..., example = ExampleSchemes.film_search), current_user: User =  Depends(get_current_active_user)): 
    """ 
    Movie search engine, Queries are immediately entered into the history (Only authorized users): 

    - **name_film**: The name of the film 
    - **genres**: List of film genres 
    - **rating_start**: Choosing a rating range from
    - **rating_end**: Selecting a rating range up to

    Returns a list of films:
    
    - **rating**: Rating of the film on IMDB 
    - **img_link**: link to the film poster from IMDB
    """    
    
    await film_crud.create_search_film(film_info, current_user)

    id_search = await film_crud.get_id_search_film(current_user)
    films_response = await search_film(film_info)

    await film_crud.create_film_history_by_search(id_search["id_search"], films_response)
    return films_response

@router.get("/history-search", response_model = list, status_code = status.HTTP_200_OK, responses =  {200: { 
 "description": "Item requested by ID", 
 "content": { 
 "application/json": { 
 "example": ExampleSchemes.search_film_request 
 }}}})
async def search_film_history(current_user: User = Depends(get_current_active_user)):
    """ 
   Query history, the last 10 are displayed (only for authorized users) 


    Returns a list of user requests:
    
    - **id_search**: id of the request in the database
    - **name_film**: The name of the film 
    - **genres**: List of film genres 
    - **rating_start**: Choosing a rating range from
    - **rating_end**: Selecting a rating range up to
    """     
    
    return await film_crud.get_history_search(current_user)

@router.get("/history-search/film-history-by-search", response_model = list[FilmHistory], status_code = status.HTTP_200_OK, responses =  {200: { 
 "description": "Item requested by ID", 
 "content": { 
 "application/json": { 
 "example": ExampleSchemes.film_response_with_id 
 }}}})
async def film_history_by_search(id_search: int, current_user: User = Depends(get_current_active_user)):
    """ 
   The first 5 films on a specific request(only authorized users): 

    - **id_search**: id of the request in the database

    Returns a list of films:

    - **name_film**: The name of the film 
    - **genres**: List of film genres 
    - **rating**: Rating of the film on IMDB 
    - **img_link**: link to the movie poster from IMDB
    """     
    
    try:
        response = await film_crud.get_history_film_by_search(id_search)
    except:
        raise HTTPException(status_code = 400, detail="films to search by id were not found")
    return response

@router.get("/selected-films", response_model = list[Film], status_code = status.HTTP_200_OK, responses =  {200: { 
 "description": "Item requested by ID", 
 "content": { 
 "application/json": { 
 "example": ExampleSchemes.film_response 
 }}}})
async def view_selected_films(current_user: User =  Depends(get_current_active_user)):
    """ 
    Viewing a list of movies from favorites (only authorized users): 


    Returns a list of films:

    - **name_film**: The name of the film 
    - **genres**: List of film genres 
    - **rating**: Rating of the film on IMDB 
    - **img_link**: link to the movie poster from IMDB
    """     

    return await film_crud.get_selected_films(current_user.login)

@router.get("/recommendations", response_model = list[Film], status_code = status.HTTP_200_OK, responses =  {200: { 
 "description": "Item requested by ID", 
 "content": { 
 "application/json": { 
 "example": ExampleSchemes.film_response 
 }}}})
async def recommendations(count_genres: int = 3, current_user: User =  Depends(get_current_active_user)):
    """ 
    Viewing movies recommendations compiled on the basis of genres of movies from favorites (only authorized users): 

    - **count_genres**: Specifying the number of genres for which films will be searched, genres are selected by the number of presence in films from favorites. The default is 3

    Returns a list of films:

    - **name_film**: The name of the film 
    - **genres**: List of film genres 
    - **rating**: Rating of the film on IMDB 
    - **img_link**: link to the movie poster from IMDB
    """ 

    return await recommend(count_genres, current_user.login)

@router.delete("/clear-history-search", status_code = status.HTTP_200_OK)
async def clear_history_search(current_user: User =  Depends(get_current_active_user)):
    """ 
    Clearing the entire query history(only authorized users) 
    """     

    return await film_crud.delete_history_search(current_user.login)

@router.delete("/selected-films/delete-selected-films", status_code = status.HTTP_200_OK)
async def delete_selected_film(id_film: int, current_user: User =  Depends(get_current_active_user)):
    """ 
    Deleting a movie from favorites(only authorized users): 

    - **id_film**: id of the selected movie in the database 
    """     
    try:
        response = await film_crud.delete_selected_film(id_film = id_film, login = current_user.login)
    except:
        raise HTTPException(status_code = 400, detail="films to search by id were not found")
    return response
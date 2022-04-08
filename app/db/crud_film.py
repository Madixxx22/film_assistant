import sqlalchemy

from app.models.film import search_film_history
from app.schemas.film import FilmFull
from app.schemas.user import User
from .base import database


class FilmCRUD():
    async def get_history_search(self, current_user: User):
        query = search_film_history.select().where(search_film_history.c.login == current_user.login)
        
        return await database.fetch_all(query)

    async def create_search_film(self, film_search: FilmFull, current_user: User):
        query = search_film_history.insert().values(login = current_user.login, name_film = film_search.name_film,
                genres = film_search.genres, rating_start = film_search.rating_start, rating_end = film_search.rating_end)
        await database.execute(query)

film_crud = FilmCRUD()
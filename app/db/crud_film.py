from re import L
import sqlalchemy

from app.models.film import search_film_history, film_history_by_search
from app.schemas.film import FilmFull
from app.schemas.user import User
from .base import database


class FilmCRUD():
    async def get_id_search_film(self, current_user: User):
        query = sqlalchemy.select([search_film_history.c.id_search]).where(
                search_film_history.c.login == current_user.login).order_by(sqlalchemy.desc(search_film_history.c.id_search))
        return await database.fetch_one(query)

    async def get_history_search(self, current_user: User):
        query = search_film_history.select().where(search_film_history.c.login == current_user.login).order_by(
            sqlalchemy.desc(search_film_history.c.id_search)).limit(10)
        return await database.fetch_all(query)

    async def get_history_film_by_search(self, id_search: int):
        query = film_history_by_search.select().where(film_history_by_search.c.id_search_film == id_search)
        return await database.fetch_all(query)

    async def create_search_film(self, film_search: FilmFull, current_user: User):
        query = search_film_history.insert().values(login = current_user.login, name_film = film_search.name_film,
                genres = film_search.genres, rating_start = film_search.rating_start, rating_end = film_search.rating_end)
        await database.execute(query)
    
    async def create_film_history_by_search(self, id_search, films):
        if len(films) <= 5:
            for i in range(len(films)):
                query = film_history_by_search.insert().values(id_search_film = id_search, name_film = films[i].name_film,
                        genres = films[i].genres, rating = films[i].rating, img_link = films[i].img_link)
                await database.execute(query)
        else:
            for i in range(5):
                query = film_history_by_search.insert().values(id_search_film = id_search, name_film = films[i].name_film,
                        genres = films[i].genres, rating = films[i].rating, img_link = films[i].img_link)
                await database.execute(query)

film_crud = FilmCRUD()
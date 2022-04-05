import requests

from app.schemas.film import Film, FilmFull
from app.core.config import API_KEY_IMDB

async def search_film(film_info: FilmFull) -> list[Film]:
    url = f'https://imdb-api.com/API/AdvancedSearch/{API_KEY_IMDB}?title={film_info.name_film}&genres={",".join(film_info.genres)}&user_rating={",".join([str(film_info.rating_start), str(film_info.rating_end)])}'

    response = requests.get(url)
    data_json = response.json()
    list_film = []
    for i in data_json:
        data = data_json[i]
        if type(data) is list:
            for j in range(len(data)):
                list_film.append(Film(name_film = data[j]["title"], genres = data[j]["genres"].split(), rating = data[j]["imDbRating"]))
    return list_film
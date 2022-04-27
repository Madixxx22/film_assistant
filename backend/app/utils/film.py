import aiohttp

from app.db.crud_film import film_crud
from app.core.config import API_KEY_IMDB
from app.schemas.film import Film, FilmSearch

#request to search for movies from the IMDB API website
async def search_film(film_info: FilmSearch) -> list[Film]:
    url = f'https://imdb-api.com/API/AdvancedSearch/{API_KEY_IMDB}?title={film_info.name_film}&user_rating={",".join([str(film_info.rating_start), str(film_info.rating_end)])}&genres={",".join(film_info.genres)}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data_json = await response.json()

    list_film = []
    for i in data_json:
        data = data_json[i]
        if type(data) is list:
            for j in range(len(data)):
                list_film.append(Film(name_film = data[j]["title"], genres = data[j]["genres"].replace(",", "").split(),
                rating = data[j]["imDbRating"], img_link = data[j]["image"]))
    return list_film

async def recommend(count_genres: int, login: str) -> list[Film]:
    selected_films = await film_crud.get_selected_films(login)
    dict_genres = {}

    #The genre and its frequency of occurrence are recorded in the dictionary
    for el in selected_films:
        for el_genr in el.genres:
            if el_genr not in dict_genres:
                dict_genres[el_genr] = 1
            
            elif el_genr in dict_genres:
                dict_genres[el_genr] += 1

    #Sorting the dictionary by genre
    sorted_dict_genres = {}
    sorted_keys = sorted(dict_genres, key=dict_genres.get) 
    sorted_keys = sorted_keys[::-1]
    for w in sorted_keys:
        sorted_dict_genres[w] = dict_genres[w]

    #Selection of genres in the sorted dictionary by frequency of occurrence
    list_genres_query = []
    if count_genres <= len(set(sorted_dict_genres.keys())):
        for i in range(count_genres):
            list_genres_query.append(list(sorted_dict_genres.keys())[i])
    else:
        for i in range(len(list(sorted_dict_genres.keys()))):
           list_genres_query.append(list(sorted_dict_genres.keys())[i])
    request_rec = FilmSearch(genres = list_genres_query)

    return await search_film(request_rec)

DESCRIPTION_APP = """
In the application, you can add movies to favorites, then, based on similar genres, you will be recommended movies that you may like. All information is obtained using the IMDB API.

## Users

You will be able to:

* **Create users**
* **Delete users**
* **Read and update profile**
* **Recover password**

## Film

You will be able to:

* **Search film**
* **Adding movies to favorites**
* **Read and clear earch history**
* **Read films by recommendation**
"""


TAGS_METADATA = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "film",
        "description": "Working with **films**, adding to favorites, viewing history, search engine, recommendations",
        "externalDocs": {
            "description": "The search engine is based on the IMDB API",
            "url": "https://imdb-api.com/api",
        },
    },
]

class ExampleSchemes():
    register = {
            "password": "123456789",
            "password_verification": "123456789",
            "email": "JoJo@example.com",
            "login": "Jostar"
    }
    
    film =   {
        "name_film": "Kingsman: The Secret Service",
        "genres": [
            "Action",
            "Adventure",
            "Comedy"
        ],
        "rating": 7.7,
        "img_link": "https://imdb-api.com/images/original/MV5BYTM3ZTllNzItNTNmOS00NzJiLTg1MWMtMjMxNDc0NmJhODU5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6837_AL_.jpg"
  }

    film_response =   [{
        "name_film": "Kingsman: The Secret Service",
        "genres": [
            "Action",
            "Adventure",
            "Comedy"
        ],
        "rating": 7.7,
        "img_link": "https://imdb-api.com/images/original/MV5BYTM3ZTllNzItNTNmOS00NzJiLTg1MWMtMjMxNDc0NmJhODU5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6837_AL_.jpg"
    },
    {
        "name_film": "Kingsman: The Golden Circle",
        "genres": [
            "Action",
            "Adventure",
            "Comedy"
        ],
        "rating": 6.7,
        "img_link": "https://imdb-api.com/images/original/MV5BMjQ3OTgzMzY4NF5BMl5BanBnXkFtZTgwOTc4OTQyMzI@._V1_Ratio0.6837_AL_.jpg"
    } ]

    film_response_with_id =   [{
        "name_film": "Kingsman: The Secret Service",
        "genres": [
            "Action",
            "Adventure",
            "Comedy"
        ],
        "rating": 7.7,
        "img_link": "https://imdb-api.com/images/original/MV5BYTM3ZTllNzItNTNmOS00NzJiLTg1MWMtMjMxNDc0NmJhODU5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_Ratio0.6837_AL_.jpg",
        "id_search_film": 1
    },
    {
        "name_film": "Kingsman: The Golden Circle",
        "genres": [
            "Action",
            "Adventure",
            "Comedy"
        ],
        "rating": 6.7,
        "img_link": "https://imdb-api.com/images/original/MV5BMjQ3OTgzMzY4NF5BMl5BanBnXkFtZTgwOTc4OTQyMzI@._V1_Ratio0.6837_AL_.jpg",
        "id_search_film": 2
    } ]

    film_search = {
        "name_film": "Kingsman",
        "genres": [
            "action", "comedy"
        ],
        "rating_start": 5.7,
        "rating_end": 8
    }

    search_film_request = [
    {
        "id_search": 1,
        "login": "Jostar",
        "name_film": "Kingsman",
        "genres": [
            "action",
            "comedy"
        ],
        "rating_start": 5.7,
        "rating_end": 8
    },
    {
        "id_search": 2,
        "login": "Jostar",
        "name_film": "Spider",
        "genres": [
            "adventure"
        ],
        "rating_start": 5,
        "rating_end": 9.6
    }]

    profile_user = {
            "email": "JoJo@example.com",
            "login": "Jostar",
            "last_name": "Joseph",
            "first_name": "Jostar",
            "registered": "2022-04-27"
    }
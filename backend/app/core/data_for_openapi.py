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


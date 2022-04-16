from os import environ
from fastapi.templating import Jinja2Templates



DB_USER = environ.get("DB_USER", "user")
DB_PASSWORD = environ.get("DB_PASSWORD", "password")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = environ.get("DB_NAME", "database")
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
API_KEY_IMDB = environ.get("API_KEY_IMDB")
GENRES = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary",
            "drama", "family", "fantasy", "film-Noir", "game-Show", "history", "horror", "music",
            "musical", "mystery", "news", "reality-TV", "romance", "sci-fi", "sport", "talk-Show",
            "thriller", "war", "western", "short"]
DATABASE_URL = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")
templates = Jinja2Templates(directory="app/templates")

from os import environ


DB_USER = environ.get("DB_USER", "user")
DB_PASSWORD = environ.get("DB_PASSWORD", "password")
DB_HOST = environ.get("DB_HOST", "localhost")
DB_NAME = environ.get("DB_NAME", "database")
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM")
API_KEY_IMDB = environ.get("API_KEY_IMDB")

GENRES = ["action", "adventure", "animation", "biography", "comedy", "crime", "documentary",
            "drama", "family", "fantasy", "film-noir", "game-show", "history", "horror", "music",
            "musical", "mystery", "news", "reality-tv", "romance", "sci-fi", "sport", "talk-show",
            "thriller", "war", "western", "short"]

DATABASE_URL = (f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}")


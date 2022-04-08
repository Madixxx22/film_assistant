import sqlalchemy

from app.db.base import metadata

films_selected = sqlalchemy.Table(
    "films_selected",
    metadata,
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login")),
    sqlalchemy.Column("name_film", sqlalchemy.String()),
    sqlalchemy.Column("genre", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("rating", sqlalchemy.Float()),
    sqlalchemy.Column("img_link", sqlalchemy.String())
    )

search_film_history = sqlalchemy.Table(
    "search_film_history",
    metadata,
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login")),
    sqlalchemy.Column("name_film", sqlalchemy.String()),
    sqlalchemy.Column("genres", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("rating_start", sqlalchemy.Float),
    sqlalchemy.Column("rating_end", sqlalchemy.Float)
)
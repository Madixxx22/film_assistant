import sqlalchemy

from app.db.base import metadata, Base

films_selected = sqlalchemy.Table(
    "films_selected",
    Base.metadata,
    sqlalchemy.Column("id_film", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login", ondelete="CASCADE")),
    sqlalchemy.Column("name_film", sqlalchemy.String()),
    sqlalchemy.Column("genres", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("rating", sqlalchemy.Float()),
    sqlalchemy.Column("img_link", sqlalchemy.String())
    )

search_film_history = sqlalchemy.Table(
    "search_film_history",
    Base.metadata,
    sqlalchemy.Column("id_search", sqlalchemy.Integer(), primary_key=True),
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login", ondelete="CASCADE")),
    sqlalchemy.Column("name_film", sqlalchemy.String()),
    sqlalchemy.Column("genres", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("rating_start", sqlalchemy.Float()),
    sqlalchemy.Column("rating_end", sqlalchemy.Float())
)

film_history_by_search = sqlalchemy.Table(
    "film_history_by_search",
    Base.metadata,
    sqlalchemy.Column("id_search_film", sqlalchemy.ForeignKey("search_film_history.id_search", ondelete="CASCADE")),
    sqlalchemy.Column("name_film", sqlalchemy.String()),
    sqlalchemy.Column("genres", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("rating", sqlalchemy.Float()),
    sqlalchemy.Column("img_link", sqlalchemy.String())
)
import sqlalchemy

from app.db.base import metadata

films_selected = sqlalchemy.Table(
    "films_selected",
    metadata,
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login")),
    sqlalchemy.Column("name_film", sqlalchemy.String()),
    sqlalchemy.Column("genre", sqlalchemy.ARRAY(sqlalchemy.String)),
    sqlalchemy.Column("rating", sqlalchemy.Float())
    )
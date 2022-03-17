import sqlalchemy

from app.db.base import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("login", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("hashed_password", sqlalchemy.String()),
)

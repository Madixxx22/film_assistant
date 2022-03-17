import sqlalchemy
from datetime import datetime

from app.db.base import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("login", sqlalchemy.String(), primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(), unique=True, nullable=False),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(), nullable=False),
)

users_authentication = sqlalchemy.Table(
    "users_authentication",
    metadata,
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login"), primary_key=True),
    sqlalchemy.Column("generated_timestamp", sqlalchemy.DateTime(), default=datetime.now),
    sqlalchemy.Column("auth_code",  sqlalchemy.String(), nullable=False),
    sqlalchemy.Column("is_used", sqlalchemy.Boolean(), default=False)
)

user_profile = sqlalchemy.Table(
    "user_profile",
    metadata,
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login"), primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String()),
    sqlalchemy.Column("last_name", sqlalchemy.String()),
    sqlalchemy.Column("registered", sqlalchemy.DateTime(), default=datetime.now)
)

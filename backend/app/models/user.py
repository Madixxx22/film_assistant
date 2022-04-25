import sqlalchemy
from datetime import date

from app.db.base import Base

users = sqlalchemy.Table(
    "users",
    Base.metadata,
    sqlalchemy.Column("login", sqlalchemy.String(), primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(), unique=True, nullable=False),
    sqlalchemy.Column("hashed_password", sqlalchemy.String(), nullable=False),
)

users_authentication = sqlalchemy.Table(
    "users_authentication",
    Base.metadata,
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("generated_timestamp", sqlalchemy.DateTime(), default=date.today),
    sqlalchemy.Column("auth_code",  sqlalchemy.String(), nullable=False),
    sqlalchemy.Column("is_used", sqlalchemy.Boolean(), default=False)
)

user_profile = sqlalchemy.Table(
    "user_profile",
    Base.metadata,
    sqlalchemy.Column("login", sqlalchemy.ForeignKey("users.login", ondelete="CASCADE"), primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String()),
    sqlalchemy.Column("last_name", sqlalchemy.String()),
    sqlalchemy.Column("registered", sqlalchemy.DateTime(), default=date.today())
)
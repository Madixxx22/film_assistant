import sqlalchemy

from .base import metadata, Base

class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)
    email = sqlalchemy.Column("email", sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column("hashed_password", sqlalchemy.String())


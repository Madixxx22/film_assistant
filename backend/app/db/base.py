from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

from backend.app.core.config import DATABASE_URL

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)

Base = declarative_base()
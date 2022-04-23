from fastapi import FastAPI

from app.db.base import database
from app.routers import users, film
from app.db.base import metadata, engine
from app.core.config import DESCRIPTION_APP


app = FastAPI(title="FilmAssistantApp", description=DESCRIPTION_APP, version="1.0.0")
app.include_router(users.router)
app.include_router(film.router)

@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect() 
import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.routers import users
from app.db.base import database
from app.db.base import metadata, engine, Base


app = FastAPI()
app.include_router(users.router)

@app.on_event("startup")
async def startup():
    await database.connect()
    metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect() 

@app.get('/')
async def test_app():
    return {"Успех" : "Успешный!"}

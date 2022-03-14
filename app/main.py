import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.routers import users
from app.db.base import database


app = FastAPI()
app.include_router(users.router)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect() 

@app.get('/')
async def test_app():
    return {"Успех" : "Успешный!"}

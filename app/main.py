import uvicorn
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.routers import users
from app.models.base import get_db


app = FastAPI()
app.include_router(users.router)

@app.get('/')
async def test_app(db: Session = Depends(get_db)):
    return {"Успех" : "Успешный!"}


if __name__ == "__main__":
    uvicorn.run("main:app", port = 8000, host = "127.0.0.1", reload = True)
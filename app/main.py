import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.get('/')
async def test_app():
    return {"Успех" : "Hello world!"}
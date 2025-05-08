from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import connect_to_mongo, close_mongo_connection
from app.routes import route as books

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="API для Бібліотеки",
    description="API для управління книгами в бібліотеці на MongoDB з FastAPI та Motor.",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(books)

@app.get("/", tags=["Головна"])
async def read_root():
    return {"message": "Вітаємо в API для Бібліотеки!"}

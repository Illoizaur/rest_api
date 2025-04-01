# lab2/app.py

from fastapi import FastAPI
from library_api.api.views import router

app = FastAPI(
    title="Library API",
    description="API для управління бібліотекою",
    version="1.0.0"
)

app.include_router(router)
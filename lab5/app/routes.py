from fastapi import APIRouter, HTTPException, status, Path
from typing import List
# from pydantic_mongo import PydanticObjectId # Не арбайтає

from app import service
from app.models import BookCreate, BookInDB, BookUpdate
# from app.database import get_book_collection

route = APIRouter(
    prefix="/rest_api/lab5/books",
    tags=["Books"],
    responses={404: {"description": "Ресурс не знайдено"}}
)

@route.post("/", response_model=BookInDB, status_code=status.HTTP_201_CREATED)
async def create_new_book(book: BookCreate):
    try:
        created_book = await service.create_book(book)
        return created_book
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Не вдалося створити книгу: {e}")

@route.get("/", response_model=List[BookInDB])
async def read_all_books(skip: int = 0, limit: int = 10):
    books = await service.get_all_books(skip=skip, limit=limit)
    return books

@route.get("/{book_id}", response_model=BookInDB)
async def read_book_by_id(
    book_id: str = Path(..., description="ID книги для отримання")
):
    book = await service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Книгу з ID '{book_id}' не знайдено")
    return book

@route.put("/{book_id}", response_model=BookInDB)
async def update_existing_book(
    book_data: BookUpdate,
    book_id: str = Path(..., description="ID книги для оновлення")
):
    existing_book = await service.get_book_by_id(book_id)
    if existing_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Книгу з ID '{book_id}' не знайдено для оновлення")

    updated_book = await service.update_book(book_id, book_data)
    if updated_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Книгу з ID '{book_id}' не знайдено після спроби оновлення")
    return updated_book

@route.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_book(
    book_id: str = Path(..., description="ID книги для видалення")
):
    existing_book = await service.get_book_by_id(book_id)
    if existing_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Книгу з ID '{book_id}' не знайдено для видалення")

    deleted_successfully = await service.delete_book(book_id)
    if not deleted_successfully:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Книгу з ID '{book_id}' не вдалося видалити або вона вже була видалена")
    return None

from fastapi import APIRouter, status, HTTPException
from typing import List
from .models import BookRepository
from .schemas import Book, BookCreate, BookUpdate


router = APIRouter(
    prefix="/books", 
    tags=["books"] 
)

book_repository = BookRepository()


@router.get("/", response_model=List[Book])
async def get_books():
    return await book_repository.get_all_books()


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = await book_repository.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return book


@router.post("/", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate):
    return await book_repository.create_book(book)


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int):
    book = await book_repository.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    await book_repository.delete_book(book_id)


@router.put("/{book_id}", response_model=Book)
async def update_book(book_id: int, book: BookUpdate):
    updated_book = await book_repository.update_book(book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail=f"Book with id {book_id} not found")
    return updated_book 
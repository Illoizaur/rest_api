from typing import List, Optional
from .schemas import Book, BookCreate, BookUpdate


class BookRepository:
    def __init__(self):
        self.books = [
            Book(
                id=1,
                title="Kobzar",
                author="Taras Schevchenko",
                isbn="9789660106123",
                published_year=1840,
                genre="Poetry",
                description="Collection of poems"
            ),
            Book(
                id=2,
                title="Eneida",
                author="Ivan Kotliarevsky",
                isbn="9789660106124",
                published_year=1798,
                genre="Poetry",
                description="Ukrainian national epic"
            )
        ]

    async def get_all_books(self) -> List[Book]:
        return self.books

    async def get_book_by_id(self, book_id: int) -> Optional[Book]:
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    async def create_book(self, book: BookCreate) -> Book:
        new_book = Book(
            id=len(self.books) + 1,
            **book.model_dump()
        )
        self.books.append(new_book)
        return new_book

    async def delete_book(self, book_id: int) -> None:
        self.books = [book for book in self.books if book.id != book_id]

    async def update_book(self, book_id: int, book: BookUpdate) -> Optional[Book]:
        for i, existing_book in enumerate(self.books):
            if existing_book.id == book_id:
                updated_book = existing_book.model_copy(update=book.model_dump(exclude_unset=True))
                self.books[i] = updated_book
                return updated_book
        return None 
from typing import List, Dict, Optional
from datetime import datetime

# Список для зберігання книг з двома прикладами
books: List[Dict] = [
    {
        "id": "1",
        "title": "Kobzar",
        "author": "Taras Schevchenko",
        "isbn": "9789660100220",
        "published_year": 1840,
        "genre": "Poetry",
        "description": "A collection of poetic works by Taras Shevchenko, which has become a symbol of Ukrainian literature."
    },
    {
        "id": "2",
        "title": "The forest song",
        "author": "Lesya Ukrainka",
        "isbn": "9789660106055",
        "published_year": 1911,
        "genre": "Drama",
        "description": "A drama-extravaganza that reflects the confrontation between high spirituality and everyday life."
    }
]

class BookRepository:
    """Репозиторій для роботи з книгами"""
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Отримати всі книги"""
        return books
    
    @staticmethod
    def get_by_id(book_id: str) -> Optional[Dict]:
        """Отримати книгу за ID"""
        for book in books:
            if book["id"] == book_id:
                return book
        return None
    
    @staticmethod
    def add(book_data: Dict) -> Dict:
        """Додати нову книгу"""
        # Якщо ID не надано, створюємо унікальний ID на основі часу
        if "id" not in book_data:
            book_data["id"] = str(int(datetime.now().timestamp()))
        
        books.append(book_data)
        return book_data
    
    @staticmethod
    def delete(book_id: str) -> bool:
        """Видалити книгу за ID"""
        for i, book in enumerate(books):
            if book["id"] == book_id:
                books.pop(i)
                return True
        return False
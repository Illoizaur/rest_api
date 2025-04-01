import pytest
from fastapi.testclient import TestClient
from fastapi import status
import sys
import os

# Додаємо кореневий шлях до Python PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Імпортуємо застосунок
from app import app

# === FIXTURES ===
@pytest.fixture
def client():
    """Клієнт для тестування API."""
    return TestClient(app)

@pytest.fixture
def test_book_data():
    """Тестові дані для створення книги."""
    return {
        "title": "Тіні забутих предків",
        "author": "Михайло Коцюбинський",
        "isbn": "9789660106123",
        "published_year": 1911,
        "genre": "Повість",
        "description": "Історія кохання на тлі гуцульських традицій"
    }

# === TEST CASES ===

def test_get_all_books(client):
    """Перевіряє отримання списку всіх книг."""
    response = client.get("/books")
    assert response.status_code == status.HTTP_200_OK
    books = response.json()
    assert isinstance(books, list)

def test_get_book_by_id(client):
    """Перевіряє отримання книги за ID."""
    response = client.get("/books/1")
    assert response.status_code == status.HTTP_200_OK
    book = response.json()
    assert book["id"] == 1
    assert book["title"] == "Kobzar"
    assert book["author"] == "Taras Schevchenko"

def test_create_book(client, test_book_data):
    """Перевіряє створення нової книги."""
    response = client.post("/books", json=test_book_data)
    assert response.status_code == status.HTTP_201_CREATED
    book = response.json()
    assert book["title"] == test_book_data["title"]
    assert book["isbn"] == test_book_data["isbn"]

def test_update_book(client):
    """Перевіряє оновлення книги."""
    update_data = {
        "description": "Оновлений опис книги"
    }
    response = client.put("/books/1", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    book = response.json()
    assert book["description"] == update_data["description"]

def test_delete_book(client):
    """Перевіряє видалення книги."""
    test_book = {
        "title": "Test Book for Delete",
        "author": "Test Author",
        "isbn": "9789660106789",
        "published_year": 2020,
        "genre": "Test",
        "description": "Test book for deletion"
    }
    create_response = client.post("/books", json=test_book)
    book_id = create_response.json()["id"]
    
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_book_not_found(client):
    """Перевіряє, що запит на неіснуючу книгу повертає 404."""
    response = client.get("/books/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_invalid_book_data(client):
    """Перевіряє валідацію помилкових даних."""
    invalid_data = {
        "title": "",  
        "author": "Test Author",
        "isbn": "123",  
        "published_year": 3000,  
        "genre": "Test"
    }
    response = client.post("/books", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

import pytest
from library_api import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_get_books(client):
    response = client.get('/api/books')
    assert response.status_code == 200
    
    # Перевірка структури відповіді
    assert isinstance(response.json, dict)
    assert 'books' in response.json
    assert isinstance(response.json['books'], list)
    assert len(response.json['books']) > 0

def test_add_book(client):
    book_data = {
        "title": "Eneyda", 
        "author": "Ivan Kotlyarevsky",
        "isbn": "9780921537663",
        "published_year": 1798
    }
    response = client.post('/api/books', json=book_data)
    assert response.status_code == 201
    
    # Перевірка структури відповіді
    assert 'book' in response.json
    assert response.json['book']['title'] == book_data["title"]
    
    # Зберігаємо ID для наступних тестів
    book_id = response.json['book']['id']
    
    # Замість return - assert
    assert book_id is not None
    return book_id

def test_get_book_by_id(client):
    # Спочатку додаємо книгу
    book_id = test_add_book(client)
    
    # Тепер отримуємо її за ID
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 200
    assert response.json['id'] == book_id

def test_delete_book(client):
    # Видаляємо книгу
    response = client.delete(f'/api/books/1')
    assert response.status_code == 200
    
    # Перевіряємо, що її більше немає
    response = client.get(f'/api/books/1')
    assert response.status_code == 404
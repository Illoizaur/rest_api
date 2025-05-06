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
    
    assert 'book' in response.json
    assert response.json['book']['title'] == book_data["title"]
    
    book_id = response.json['book']['id']
    
    assert book_id is not None
    return book_id

def test_get_book_by_id(client):
    book_id = test_add_book(client)
    
    response = client.get(f'/api/books/{book_id}')
    assert response.status_code == 200
    assert response.json['id'] == book_id

def test_delete_book(client):
    response = client.delete(f'/api/books/1')
    assert response.status_code == 200
    
    response = client.get(f'/api/books/1')
    assert response.status_code == 404

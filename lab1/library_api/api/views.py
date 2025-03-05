# library_api/api/views.py
from typing import Tuple, Dict, Any
from flask import Blueprint, request, jsonify, Response, url_for
from marshmallow import ValidationError

from .models import BookRepository
from .schemas import BookSchema

# Створення blueprint для API
api = Blueprint('api', __name__)

# Ініціалізація схеми валідації
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@api.route('/books', methods=['GET'])
def get_books() -> Tuple[Response, int]:
    """Отримати всі книги"""
    all_books = BookRepository.get_all()
    result = books_schema.dump(all_books)
    
    # Створюємо обгортку з гіперпосиланнями
    base_url = request.url_root.rstrip('/') + '/api'
    response = {
        "books": result,
        "_links": {
            "self": f"{base_url}/books",
            "add": f"{base_url}/books"
        },
        "total": len(result)
    }
    
    return jsonify(response), 200

@api.route('/books/<book_id>', methods=['GET'])
def get_book(book_id: str) -> Tuple[Response, int]:
    """Отримати книгу за ID"""
    book = BookRepository.get_by_id(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    
    result = book_schema.dump(book)
    return jsonify(result), 200

@api.route('/books', methods=['POST'])
def add_book() -> Tuple[Response, int]:
    """Додати нову книгу"""
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400
    
    # Валідація даних за допомогою Marshmallow
    try:
        book_data = book_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"error": "Validation error", "messages": err.messages}), 400
    
    # Додавання книги
    new_book = BookRepository.add(book_data)
    result = book_schema.dump(new_book)
    
    # Додаємо інформацію про створений ресурс та посилання
    base_url = request.url_root.rstrip('/') + '/api'
    response = {
        "message": "Book created successfully",
        "book": result,
        "_links": {
            "self": f"{base_url}/books/{result['id']}",
            "collection": f"{base_url}/books"
        }
    }
    
    return jsonify(response), 201

@api.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id: str) -> Tuple[Response, int]:
    """Видалити книгу за ID"""
    if BookRepository.delete(book_id):
        # Повертаємо посилання на колекцію після видалення
        response = {
            "message": "Book deleted successfully",
            "_links": {
                "collection": url_for('api.get_books', _external=True)
            }
        }
        return jsonify(response), 200
    
    return jsonify({"error": "Book not found"}), 404

@api.route('/', methods=['GET'])
def api_root() -> Tuple[Response, int]:
    """Кореневий ендпоінт API з інформацією про доступні ресурси"""
    base_url = request.url_root.rstrip('/') + '/api'
    response = {
        "name": "Library API",
        "version": "1.0",
        "_links": {
            "books": {
                "href": f"{base_url}/books",
                "methods": ["GET", "POST"]
            },
            "book": {
                "href": f"{base_url}/books/{{book_id}}",
                "templated": True,
                "methods": ["GET", "DELETE"]
            }
        }
    }
    return jsonify(response), 200
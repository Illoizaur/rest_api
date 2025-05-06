from flask import Blueprint, request, jsonify, Response, url_for
from marshmallow import ValidationError
from typing import Tuple

from .models import db, Book
from .schemas import BookSchema
from .errors import books_not_found, invalid_data, validation_error, book_not_found

api = Blueprint('api', __name__)

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@api.route('/books', methods=['GET'])
def get_books() -> Tuple[Response, int]:
    limit = request.args.get("limit", default=10, type=int)
    cursor_after = request.args.get("cursor", type=int)
    cursor_before = request.args.get("before", type=int)

    base_url = request.url_root.rstrip('/') + '/api'

    # Сортуємо і фільтруємо залежно від напрямку пагінації
    if cursor_after:
        query = Book.query.filter(Book.id > cursor_after).order_by(Book.id.asc())
    elif cursor_before:
        query = Book.query.filter(Book.id < cursor_before).order_by(Book.id.desc())
    else:
        query = Book.query.order_by(Book.id.asc())

    books = query.limit(limit).all()

    if not books:
        return books_not_found()

    if cursor_before:
        books.reverse()

    result = books_schema.dump(books)

    next_cursor = books[-1].id if len(books) == limit else None
    prev_cursor = books[0].id if cursor_after or cursor_before else None

    links = {
        "self": request.url,
        "add": f"{base_url}/books"
    }

    if next_cursor:
        links["next"] = f"{base_url}/books?limit={limit}&cursor={next_cursor}"
    if prev_cursor and (cursor_after or cursor_before):
        links["prev"] = f"{base_url}/books?limit={limit}&before={prev_cursor}"

    response = {
        "books": result,
        "_links": links,
        "total": Book.query.count()
    }

    return jsonify(response), 200

@api.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id: int) -> Tuple[Response, int]:
    book = Book.query.get(book_id)
    if book is None:
        return book_not_found()

    result = book_schema.dump(book)
    total_books = Book.query.count()

    base_url = request.url_root.rstrip('/') + '/api/books'
    response = {
        "book": result,
        "_links": {
            "self": f"{base_url}/{book_id}",
            "collection": f"{base_url}",
        }
    }

    if book_id > 1:
        response["_links"]["previous"] = f"{base_url}/{book_id - 1}"

    if book_id < total_books:
        response["_links"]["next"] = f"{base_url}/{book_id + 1}"

    return jsonify(response), 200

@api.route('/books', methods=['POST'])
def add_book() -> Tuple[Response, int]:
    json_data = request.get_json()
    if not json_data:
        return invalid_data()

    try:
        book_data = book_schema.load(json_data)
    except ValidationError as err:
        return validation_error()

    new_book = Book(**book_data)
    db.session.add(new_book)
    db.session.commit()

    result = book_schema.dump(new_book)
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
    book = Book.query.get(book_id)
    if not book:
        return book_not_found()

    db.session.delete(book)
    db.session.commit()

    response = {
        "message": "Book deleted successfully",
        "_links": {
            "collection": url_for('api.get_books', _external=True)
        }
    }
    return jsonify(response), 200


@api.route('/', methods=['GET'])
def api_root() -> Tuple[Response, int]:
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

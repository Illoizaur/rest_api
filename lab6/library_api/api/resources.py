from flask_restful import Resource, reqparse
from flask import request, url_for
from marshmallow import ValidationError
from .models import db, Book
from .schemas import BookSchema
from .errors import *

book_schema = BookSchema()
books_schema = BookSchema(many=True)

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('author', required=True)
parser.add_argument('isbn')
parser.add_argument('published_year', type=int)
parser.add_argument('genre')
parser.add_argument('description')

class BookCollection(Resource):
    def get(self):
        """
        Get all books with pagination
        ---
        tags:
          - Books
        parameters:
          - name: limit
            in: query
            type: integer
            default: 10
          - name: cursor
            in: query
            type: integer
          - name: before
            in: query
            type: integer
        responses:
          200:
            description: List of books
            schema:
              $ref: '#/definitions/BookCollection'
          404:
            description: No books found
        """
        args = request.args
        limit = args.get('limit', 10, type=int)
        cursor_after = args.get('cursor', type=int)
        cursor_before = args.get('before', type=int)

        query = Book.query
        if cursor_after:
            query = query.filter(Book.id > cursor_after).order_by(Book.id.asc())
        elif cursor_before:
            query = query.filter(Book.id < cursor_before).order_by(Book.id.desc())
        else:
            query = query.order_by(Book.id.asc())

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
            "add": "/api/books"
        }
        if next_cursor:
            links["next"] = f"/api/books?limit={limit}&cursor={next_cursor}"
        if prev_cursor:
            links["prev"] = f"/api/books?limit={limit}&before={prev_cursor}"

        return {
            "books": result,
            "_links": links,
            "total": Book.query.count()
        }, 200

    def post(self):
        """
        Create new book
        ---
        tags:
          - Books
        parameters:
          - name: body
            in: body
            required: true
            schema:
              $ref: '#/definitions/BookInput'
        responses:
          201:
            description: Book created
            schema:
              $ref: '#/definitions/Book'
          400:
            description: Validation error
          422:
            description: Invalid data
        """
        data = parser.parse_args()
        try:
            book_data = book_schema.load(data)
        except ValidationError as err:
            return validation_error()

        new_book = Book(**book_data)
        db.session.add(new_book)
        db.session.commit()

        result = book_schema.dump(new_book)
        result['_links'] = {
            "self": f"/api/books/{result['id']}",
            "collection": "/api/books"
        }
        return {"message": "Book created", "book": result}, 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Get single book
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Book details
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Book not found
        """
        book = Book.query.get(book_id)
        if not book:
            return book_not_found()

        result = book_schema.dump(book)
        total = Book.query.count()
        links = {
            "self": f"/api/books/{book_id}",
            "collection": "/api/books"
        }
        if book_id > 1:
            links["previous"] = f"/api/books/{book_id-1}"
        if book_id < total:
            links["next"] = f"/api/books/{book_id+1}"

        return {"book": result, "_links": links}, 200

    def put(self, book_id):
            """
            Оновити книгу
            ---
            tags:
              - Books
            parameters:
              - name: book_id
                in: path
                type: integer
                required: true
              - name: body
                in: body
                required: true
                schema:
                  $ref: '#/definitions/BookInput'
            responses:
              200:
                description: Книга оновлена
                schema:
                  $ref: '#/definitions/Book'
              400:
                description: Помилка валідації
              404:
                description: Книга не знайдена
            """
            data = request.get_json()
            if not data:
                return {"message": "Invalid input"}, 400

            try:
                book_data = book_schema.load(data)
            except ValidationError as err:
                return {"message": "Validation error", "errors": err.messages}, 400

            book = Book.query.get(book_id)
            if not book:
                return {"message": "Book not found"}, 404

            # Оновлюємо поля
            book.title = book_data.get('title', book.title)
            book.author = book_data.get('author', book.author)
            book.isbn = book_data.get('isbn', book.isbn)
            book.published_year = book_data.get('published_year', book.published_year)
            book.genre = book_data.get('genre', book.genre)
            book.description = book_data.get('description', book.description)

            db.session.commit()

            result = book_schema.dump(book)
            return {"message": "Book updated", "book": result}, 200

    def delete(self, book_id):
        """
        Delete book
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
        responses:
          200:
            description: Book deleted
          404:
            description: Book not found
        """
        book = Book.query.get(book_id)
        if not book:
            return book_not_found()

        db.session.delete(book)
        db.session.commit()
        return {"message": "Book deleted", "_links": {"collection": "/api/books"}}, 200

class APIRoot(Resource):
    def get(self):
        """
        API Root
        ---
        tags:
          - Meta
        responses:
          200:
            description: API entry point
        """
        return {
            "name": "Library API",
            "version": "1.0",
            "_links": {
                "books": {
                    "href": "/api/books",
                    "methods": ["GET", "POST"]
                },
                "book": {
                    "href": "/api/books/{book_id}",
                    "templated": True,
                    "methods": ["GET", "DELETE"]
                }
            }
        }, 200

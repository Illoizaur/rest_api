from flask_restful import abort

def books_not_found():
    abort(404, message="No books found")

def book_not_found():
    abort(404, message="Book not found")

def invalid_data():
    abort(422, message="Invalid data")

def validation_error():
    abort(400, message="Validation error")

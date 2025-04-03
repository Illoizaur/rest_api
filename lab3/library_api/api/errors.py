# library_api/api/errors.py

from flask import jsonify
from marshmallow import ValidationError

def books_not_found():
	return jsonify({"error": "Not books found"})

def book_not_found():
	return jsonify({"error": "Book not found"})

def invalid_data():
	return jsonify({"error": "Book not found"})

def validation_error():
	return jsonify({"error": "Validation error", "messages": err.messages, status: 400})

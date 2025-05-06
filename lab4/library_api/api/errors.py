from flask import jsonify

def books_not_found():
	return jsonify({"error": "Not books found"}), 404

def book_not_found():
	return jsonify({"error": "Book not found"}), 404

def invalid_data():
	return jsonify({"error": "Invalid data"}), 422

def validation_error():
	return jsonify({"error": "Validation error"}), 400

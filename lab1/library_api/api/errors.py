from typing import Dict, Any
from flask import jsonify
from marshmallow import ValidationError

def register_error_handlers(app):
    """Реєстрація обробників помилок"""
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Обробка помилок валідації"""
        return jsonify({"error": "Validation error", "messages": error.messages}), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Обробка помилки 'не знайдено'"""
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def handle_server_error(error):
        """Обробка внутрішніх помилок сервера"""
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Обробка помилки 'метод не дозволено'"""
        return jsonify({"error": "Method not allowed"}), 405
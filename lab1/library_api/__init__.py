from flask import Flask
from typing import Optional

def create_app(test_config: Optional[dict] = None) -> Flask:
    """Фабрика для створення Flask додатку"""
    # Створення екземпляру Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # Базова конфігурація
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    
    if test_config is not None:
        # Тестова конфігурація
        app.config.from_mapping(test_config)
    
    # Реєстрація ендпоінтів API
    from .api.views import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Реєстрація обробників помилок
    from .api.errors import register_error_handlers
    register_error_handlers(app)
    
    @app.route('/')
    def index():
        """Головна сторінка"""
        return {"message": "Welcome to Library API"}
    
    return app
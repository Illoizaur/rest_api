from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from typing import Optional
from .api.models import init_db

def create_app(test_config: Optional[dict] = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is not None:
        app.config.from_mapping(test_config)

    from .api.views import api
    app.register_blueprint(api, url_prefix='/api')

    init_db(app)

    @app.route('/')
    def index():
        return {"message": "Welcome to Library API"}

    return app

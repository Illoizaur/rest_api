from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from library_api.api.models import db
from library_api.api.resources import BookCollection, BookResource, APIRoot

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    api = Api(app)
    api.add_resource(APIRoot, '/api')
    api.add_resource(BookCollection, '/api/books')
    api.add_resource(BookResource, '/api/books/<int:book_id>')

    Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "version": "1.0",
            "description": "API for managing library books"
        },
        "definitions": {
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "isbn": {"type": "string"},
                    "published_year": {"type": "integer"},
                    "genre": {"type": "string"},
                    "description": {"type": "string"},
                    "_links": {
                        "type": "object",
                        "properties": {
                            "self": {"type": "string"},
                            "collection": {"type": "string"}
                        }
                    }
                }
            },
            "BookInput": {
                "type": "object",
                "required": ["title", "author"],
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "isbn": {"type": "string"},
                    "published_year": {"type": "integer"},
                    "genre": {"type": "string"},
                    "description": {"type": "string"}
                }
            },
            "BookCollection": {
                "type": "object",
                "properties": {
                    "books": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Book"}
                    },
                    "_links": {
                        "type": "object",
                        "properties": {
                            "self": {"type": "string"},
                            "next": {"type": "string"},
                            "prev": {"type": "string"},
                            "add": {"type": "string"}
                        }
                    },
                    "total": {"type": "integer"}
                }
            }
        }
    })

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

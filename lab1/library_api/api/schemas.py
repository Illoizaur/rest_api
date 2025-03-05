# library_api/api/schemas.py
from marshmallow import Schema, fields, validate, ValidationError, post_dump
from datetime import datetime
from flask import request

class BookSchema(Schema):
    """Схема для валідації книги"""
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=100))
    author = fields.String(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.String(validate=validate.Length(equal=13))
    published_year = fields.Integer(validate=validate.Range(min=1000, max=datetime.now().year))
    genre = fields.String(validate=validate.Length(min=1, max=50))
    description = fields.String(validate=validate.Length(max=1000))
    
    # Поле для гіперпосилань
    _links = fields.Dict(dump_only=True)
    
    @post_dump
    def add_links(self, data, **kwargs):
        """Додавання гіперпосилань до відповіді"""
        book_id = data.get('id')
        if book_id:
            # Генеруємо посилання вручну, без url_for
            base_url = request.url_root.rstrip('/') + '/api'
            data['_links'] = {
                'self': f"{base_url}/books/{book_id}",
                'collection': f"{base_url}/books"
            }
        return data

    class Meta:
        ordered = True
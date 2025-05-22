from marshmallow import Schema, fields, validate, post_dump
from datetime import datetime

class BookSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=255))
    author = fields.String(required=True, validate=validate.Length(min=1, max=255))
    isbn = fields.String(validate=validate.Length(equal=13))
    published_year = fields.Integer(validate=validate.Range(min=1000, max=datetime.now().year))
    genre = fields.String(validate=validate.Length(min=1, max=50))
    description = fields.String(validate=validate.Length(max=1000))

    @post_dump
    def add_links(self, data, **kwargs):
        data['_links'] = {
            'self': f"/api/books/{data['id']}",
            'collection': "/api/books"
        }
        return data

    class Meta:
        ordered = True

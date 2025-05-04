from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

db = SQLAlchemy()

class Book(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(255), nullable = False)
	author = db.Column(db.String(255), nullable = False)
	isbn = db.Column(db.String(13), unique = True, nullable = False)
	published_year = db.Column(db.Integer, nullable = False)
	genre = db.Column(db.String(50), nullable = False)
	description = db.Column(db.Text, nullable = True)

def init_db(app: Flask):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/library")
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.init_app(app)
	with app.app_context():
		db.create_all()

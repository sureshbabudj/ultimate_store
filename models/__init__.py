from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .book import Book, readership
from .user import User
from .author import Author

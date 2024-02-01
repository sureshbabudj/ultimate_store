from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import db

# Association table for the many-to-many relationship between User and Book
readership = Table('readership', db.Model.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('book_id', Integer, ForeignKey('book.id'))
)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    published_date = db.Column(db.Date, nullable=True)
    openlibrary_lending_url = db.Column(db.String(200), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship('Author', back_populates='books')
    readers = relationship('User', secondary=readership, back_populates='books_read')

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.price})"

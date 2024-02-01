from datetime import datetime
from sqlalchemy.orm import relationship

from . import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    books_count = db.Column(db.Integer, default=0)

    books = relationship('Book', back_populates='author')

    def __repr__(self):
        return f"Author('{self.name}')"
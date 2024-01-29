from flask import flash, render_template, request
from models import Book
from sqlalchemy.exc import SQLAlchemyError
from . import shop

@shop.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 8, type=int)

    try:
        books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    except SQLAlchemyError as e:
        flash(f'Database error: {str(e)}', 'error')
        books = []

    return render_template('home.html', books=books.items, current_page=page, total_pages=books.pages)

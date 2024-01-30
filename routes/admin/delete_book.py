from flask import flash, redirect, url_for
from models import db, Book
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required
from . import admin

@admin.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
    except SQLAlchemyError as e:
        flash(f'Database error: {str(e)}', 'danger')

    return redirect(url_for('admin.index'))
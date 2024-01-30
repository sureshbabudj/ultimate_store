from flask import render_template, flash, redirect, url_for
from models import db, Book
from forms import BookForm
from sqlalchemy.exc import SQLAlchemyError

from . import admin

@admin.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        try:
            book.title = form.title.data
            book.author = form.author.data
            book.price = form.price.data
            book.image_url = form.image_url.data
            db.session.commit()
        except SQLAlchemyError as e:
            flash(f'Database error: {str(e)}', 'danger')

        return redirect(url_for('admin.index'))

    return render_template('edit_book.html', form=form, book=book)
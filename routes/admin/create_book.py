from flask import render_template, flash, redirect, url_for
from decorators import admin_required
from models import db, Book
from forms import BookForm
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required

from . import admin

@admin.route('/create_book', methods=['GET', 'POST'])
@login_required
@admin_required
def create_book():
    form = BookForm()

    if form.validate_on_submit():
        try:
            existing_book = Book.query.filter_by(title=form.title.data).first()
            if existing_book:
                flash('Book with the same title already exists. Choose a different title.', 'danger')
            else:
                new_book = Book(
                    title=form.title.data,
                    author=form.author.data,
                    price=form.price.data,
                    image_url=form.image_url.data,
                )
                db.session.add(new_book)
                db.session.commit()
                flash('Book added successfully!', 'success')
        except SQLAlchemyError as e:
            flash(f'Database error: {str(e)}', 'danger')

        return redirect(url_for("admin.index"))
    
    return render_template("create_book.html", form=form,)
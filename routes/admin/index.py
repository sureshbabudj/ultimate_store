from flask import render_template, flash, redirect, url_for
from forms import BookForm
from models import db, Book
from sqlalchemy.exc import SQLAlchemyError
from . import admin

@admin.route("/", methods=["GET", "POST"])
def index():
    try:
        books = Book.query.all()
    except SQLAlchemyError as e:
        flash(f'Database error: {str(e)}', 'danger')
        books = []

    return render_template("admin.html", books=books)
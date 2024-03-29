from flask import render_template, flash, redirect, url_for
from decorators import admin_required
from models import Book, User
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_required
from . import admin

@admin.route("/", methods=["GET", "POST"])
@login_required
@admin_required
def index():
    try:
        books = Book.query.all()
        users = User.query.all()
    except SQLAlchemyError as e:
        flash(f'Database error: {str(e)}', 'danger')
        books = []

    return render_template("admin.html", books=books, users=users)
from flask import Blueprint
admin = Blueprint('admin', __name__)

from . import delete_book, edit_book, index




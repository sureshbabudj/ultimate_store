import os
from dotenv import load_dotenv
import secrets
from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import BookForm

# Load environment variables from .env
load_dotenv()

# Print the loaded environment variables
print("Loaded environment variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

app = Flask(__name__)

# Use environment variables for sensitive information
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', "postgresql://admin:root@localhost/ultimate_store")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.price})"

@app.route("/admin", methods=["GET", "POST"])
def admin():
    form = BookForm()

    if form.validate_on_submit():
        # Check if a book with the same title already exists
        existing_book = Book.query.filter_by(title=form.title.data).first()
        if existing_book:
            flash('Book with the same title already exists. Choose a different title.', 'error')
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
        return redirect(url_for("home"))

    books = Book.query.all()
    return render_template("admin.html", form=form, books=books)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.price = form.price.data
        book.image_url = form.image_url.data
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit_book.html', form=form, book=book)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True)


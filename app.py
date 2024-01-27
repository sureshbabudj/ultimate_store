import os
from datetime import datetime
from dotenv import load_dotenv
import secrets
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_assets import Environment, Bundle
from forms import BookForm

# Load environment variables from .env
load_dotenv()

# Print the loaded environment variables
print("Loaded environment variables:")
print(f"FLASK_SECRET_KEY: {os.environ.get('FLASK_SECRET_KEY')}")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")

app = Flask(__name__)

# Use environment variables for sensitive information
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', "postgresql://admin:root@localhost/ultimate_store")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Assets
assets = Environment()
assets.init_app(app)

# Define CSS and JS bundles with minification
css_bundle = Bundle(
    'css/bootstrap.css',
    'css/font-awesome.min.css',
    'css/owl.carousel.css',
    'css/responsive.css',
    'css/style.css',
    filters='cssmin',  # Apply CSS minification
    output='gen/packed.css'
)

js_bundle = Bundle(
    'js/bootstrap.js',
    'js/bxslider.min.js',
    'js/jquery.easing.1.3.min.js',
    'js/jquery.sticky.js',
    'js/main.js',
    'js/owl.carousel.min.js',
    'js/script.slider.js',
    filters='jsmin',  # Apply JS minification
    output='gen/packed.js'
)

# Register the bundles
assets.register('css_all', css_bundle)
assets.register('js_all', js_bundle)

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
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('limit', 8, type=int)  

    books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Calculate the total number of pages
    total_books = Book.query.count()
    total_pages = (total_books // per_page) + (1 if total_books % per_page > 0 else 0)

    return render_template('home.html', books=books.items, current_page=page, total_pages=total_pages)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True)


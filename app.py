import os
import secrets
from flask import Flask, flash, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import BookForm

app = Flask(__name__)

# Use environment variables for sensitive information
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))

# Configure the database URI based on the environment
if app.env == 'production':
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')  # Use Heroku-provided DATABASE_URL for production
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

# Suppress a warning about track modifications, it's not needed for now
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

# ... (rest of your routes remain unchanged)

# Manually create tables within the application context
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    import sys

    if '--env=production' in sys.argv:
        # In production, use a production-ready server like Gunicorn
        import os
        from gunicorn import GunicornApplication

        class StandaloneApplication(GunicornApplication):
            def init(self, parser, opts, args):
                return {
                    'bind': f"0.0.0.0:{int(os.environ.get('PORT', 5000))}",
                    'workers': 1
                }

        options = {
            'bind': '0.0.0.0:5000',
            'workers': 1,
        }
        StandaloneApplication(app, options).run()
    else:
        # In development, use the Flask development server
        app.run(debug=True)


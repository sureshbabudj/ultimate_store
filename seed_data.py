from psycopg2 import IntegrityError
import requests
import random
from models import db, Book, User

def get_book_cover(isbn):
    base_url = "http://covers.openlibrary.org/b/id/"
    response = requests.get(f"{base_url}{isbn}-L.jpg")

    if response.status_code == 200:
        return response.url
    else:
        return None

def get_books_from_open_library():
    # Use the Open Library API to get a list of books
    api_url = "https://openlibrary.org/subjects/fiction.json"
    response = requests.get(api_url)
    data = response.json()

    # Extract book information
    books = []
    for work in data.get("works", []):
        title = work.get("title", "Unknown Title")
        authors = work.get("authors", [])
        author = authors[0].get("name") if authors else "Unknown Author"
        price = round(random.uniform(10, 100), 2)  # Generate a random price
        isbn = work.get("cover_id", "")  # Use cover edition key as ISBN
        image_url = get_book_cover(isbn)  # Get cover image URL

        books.append(Book(title=title, author=author, price=price, image_url=image_url))

    return books

def generate_fake_users(num_users):
    users = []
    for num in range(num_users):
        email = f"user{num}@example.com"
        password = 'test123'
        user = User(email=email)
        user.set_password(password)
        users.append(user)

    return users

def seed_users():
    try:
        # Seed fake users
        users = generate_fake_users(num_users=5)

        db.session.add_all(users)
        db.session.commit()  
    except IntegrityError as e:
        # Handle the IntegrityError
        db.session.rollback()  # Rollback the transaction
        print(f"Error: {e}")
        print("User with the same email already exists. Skipping user creation.")
    except Exception as e:
        # Handle other exceptions
        db.session.rollback()  # Rollback the transaction
        print(f"Error: {e}")
        print("An error occurred while creating users.")

def seed_data():
    # Check if there are any existing records in the Book and User tables
    #if not db.session.query(Book).count() and not db.session.query(User).count():
    try:
        # Seed books from Open Library API
        books = get_books_from_open_library()

        # Seed additional books if needed
        additional_books = [
            # Book(title="Another Book", author="Another Author", price=24.99, image_url="book3.jpg"),
            # Add more books as needed
        ]

        db.session.add_all(books + additional_books)
        db.session.commit()
    except IntegrityError as e:
        # Handle the IntegrityError
        db.session.rollback()  # Rollback the transaction
        print(f"Error: {e}")
        print("Book with the same title already exists. Skipping book creation.")
    except Exception as e:
        # Handle other exceptions
        db.session.rollback()  # Rollback the transaction
        print(f"Error: {e}")
        print("An error occurred while creating users.")

if __name__ == '__main__':
    seed_data()
    seed_users()

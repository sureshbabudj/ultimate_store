from datetime import datetime
import json
import random
import requests
from models import db, Book, Author, User, readership
from sqlalchemy.exc import IntegrityError

genres = ["Fiction", "Non-fiction", "Science Fiction", "Mystery", "Fantasy", "Romance", "Thriller", "Biography", "History"]

def write_open_lib_json():
    responses = {}

    for genre in genres:
        response = requests.get(f"https://openlibrary.org/subjects/{genre.lower()}.json")
        responses[genre] = response.json()

    # Write responses to a JSON file
    with open('api_responses.json', 'w') as json_file:
        json.dump(responses, json_file)

authors = []

def generate_authors(authors_data):
    author_name = authors_data[0].get("name")
    book_author = None 
    added_authors = set()

    book_author = Author(name=author_name)
    
    # Check if the book title is not already added
    if book_author not in added_authors:
         # Add the title to the set
        added_authors.add(author_name)
        authors.append(book_author)

    return book_author



def get_book_cover(isbn):
    base_url = "http://covers.openlibrary.org/b/id/"
    response = requests.get(f"{base_url}{isbn}-L.jpg")

    if response.status_code == 200:
        return response.url
    else:
        return None

def get_book_data_json(response):
    try:
        books_data = response.json().get("works", [])
        return books_data
    except requests.JSONDecodeError as json_error:
        print(f"JSON decoding error: {json_error}")
        print(f"Response content: {response.content}")
        return []

def get_book_data_json():
    try:
        with open('api_responses.json', 'r') as json_file:
            stored_responses = json.load(json_file)
            return stored_responses
    except FileNotFoundError:
        print("File not found. Make sure to run the script that generates 'api_responses.json' first.")
        return {}
    

def generate_books():
    stored_responses = get_book_data_json()
    
    books = []
    added_titles = set()
    for genre in genres:
        books_data = stored_responses.get(genre, {}).get("works", [])
        for book_data in books_data:
            # Aggregate Authors
            
            author = generate_authors(book_data.get("authors", []))

            # Aggregate Books
            title = book_data.get("title", "Unknown Title")

            # Check if the book title is not already added
            if title not in added_titles:
                description = book_data.get("description", "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque egestas, nisl nec maximus elementum, tortor metus egestas ipsum, vehicula commodo odio enim ut eros. Integer dapibus lorem nisl, vel ornare lacus tincidunt non. Morbi tempus facilisis quam feugiat auctor. Quisque a elit justo. Nam at elit nisl.") 
                published_date = book_data.get("first_publish_year", None)
                openlibrary_lending_url = f"https://openlibrary.org/works/{book_data.get('key', '')}"
                image_url = get_book_cover(book_data.get("cover_id", ""))
                price = round(random.uniform(10, 100), 2)

                book = Book(
                    title=title,
                    author=author,
                    genre=genre,
                    price=price,
                    description=description,
                    published_date=datetime.strptime(str(published_date), "%Y") if published_date else None,
                    openlibrary_lending_url=openlibrary_lending_url,
                    image_url=image_url,
                    created_on=datetime.utcnow(),
                    updated_on=datetime.utcnow()
                )
                
                # Add the title to the set
                added_titles.add(title)
                books.append(book)

    return books


# Function to generate users
def generate_users():
    added_users = set()
    #countries
    countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua", "and", "Barbuda", "Argentina", "Armenia", 
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", 
    "Bhutan", "Bolivia", "Bosnia", "and", "Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina", "Faso", "Burundi", 
    "Côte", "d'Ivoire", "Cabo", "Verde", "Cambodia", "Cameroon", "Canada", "Central", "African", "Republic", "Chad", "Chile", 
    "China", "Colombia", "Comoros", "Congo", "(Congo-Brazzaville)", "Costa", "Rica", "Croatia", "Cuba", "Cyprus", "Czechia", 
    "Czech", "Republic", "Democratic", "Republic", "of", "the", "Congo", "Denmark", "Djibouti", "Dominica", "Dominican", "Republic"]

    streets = ["New Street", "MG Road", "MarbachWeg", "BlutenStr", "Villa Bambina cross", "Red Cross Road"]

    cities = ["Baveria", "Naveda", "Arizone", "Delhi", "Coimbatore"]

    # Sample first names and last names
    first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack",
                "Katherine", "Leo", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rose", "Samuel", "Tara"]

    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
                "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"]

    users = []

    for i in range(40):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        email = f"{first_name.lower()}.{last_name.lower()}@example.com"

        if email not in added_users:
            name=f"{first_name} {last_name}"
            password = 'test123'
            address = f"{i + 1} {random.choice(streets)}, {random.choice(cities)}, {random.choice(countries)}" # generate city, country somewhat aligning
            phone_number = f"+1-555-555-{i + 1000}" # generate random number based city, country

            user = User(
                name=name,
                email=email,
                address=address,
                phone_number=phone_number,
                created_on=datetime.utcnow(),
                updated_on=datetime.utcnow()
            )

            user.set_password(password)

             # Add the email to the set
            added_users.add(email)
            users.append(user)

    return users

# Function to seed data
def seed_data():

    # create file
    write_open_lib_json()

    # Seed book and author data from Open Library API
    books = generate_books()


    # Generate users
    users = generate_users()

    
    try:
        # Add authors and books to the database
        db.session.add_all(authors)
        db.session.add_all(books)

        # Commit authors and books
        db.session.commit()

        # Add users to the database
        db.session.add_all(users)

        db.session.commit()

        # Fetch all users
        users = User.query.all()

        # Assign random books to users (for testing purposes)
        for user in users:
            user_books = Book.query.order_by(db.func.random()).limit(5).all()
            user.books_read.extend(user_books)

        # Commit the changes to the database
        db.session.commit()

    except IntegrityError as e:
        db.session.rollback()
        print(f"Error: {e}")

        # Log the specific error, handle unique constraint violation
        if "unique constraint" in str(e):
            print("Unique constraint violation, skipping duplicate entry.")
        else:
            raise  # Re-raise other IntegrityError types

# Run the seed data function
if __name__ == "__main__":
    seed_data()

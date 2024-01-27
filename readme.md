
# Ultimate Bookstore

This is a simple Flask application for a children's bookstore with the ability to add books. It uses Flask-SQLAlchemy for database management and Flask-Migrate for handling database migrations.

## Getting Started

Follow these steps to set up and run the Flask application.

### Prerequisites

- Python 3.x
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sureshbabudj/ultimate_store.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd ultimate_store
   ```

3. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Database Migration

Before running the application, perform the following database migration steps:

1. **Initialize Flask-Migrate:**

   ```bash
   flask db init
   ```

2. **Generate a migration script:**

   ```bash
   flask db migrate -m "{SOME_COMMENT}"
   ```

3. **Apply the migration:**

   ```bash
   flask db upgrade
   ```

### Running the Application

Now, you can run the Flask application:

```bash
python app.py
```

The application should be accessible at `http://127.0.0.1:5000/`.

### Admin Page

Visit the admin page to add books:

- URL: `http://127.0.0.1:5000/admin`

### Deactivate Virtual Environment

When you're done using the application, deactivate the virtual environment:

```bash
deactivate
```


### Env Variables

FLASK_SECRET_KEY={HEX16}
DATABASE_URL={DB}
FLASK_ENV={production|dev}


### Creat database in postgres sql

```psql
CREATE DATABASE ultimate_store;
CREATE USER admin WITH PASSWORD 'root';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ultimate_store TO admin;

```

## Author

Suresh Babu Dhanaraj

- GitHub: [sureshbabudj](https://github.com/sureshbabudj)
- Email: sureshbabudj@gmail.com




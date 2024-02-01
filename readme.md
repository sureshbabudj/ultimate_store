# Ultimate Bookstore

This is a simple Flask application for a bookstore with the ability to add books. It uses Flask-SQLAlchemy for database management and Flask-Migrate for handling database migrations.

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

     make sure to execute below command in Powershell to activate virtual env

     ```bash
     Set-ExecutionPolicy Unrestricted -Scope Process
     ```

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**

   for installing  the main dependencies, :

   ```bash
   pip install -r requirements.txt
   ```

   and for installing dev dependencies for development, use:

   ```bash
   pip install -r requirements-dev.txt 
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

### File Watcher for CSS and JS Files

This Python script (`watcher.py`) monitors changes to CSS and JS files in a specified directory and automatically runs the `bundle.py` script to update the compressed and combined versions of these files. It uses the `watchdog` library to detect file modifications.

### How to Use

```bash
pip install watchdog
```

### Usage

1. Place the `watcher.py` script in your project directory.
2. Open a terminal and navigate to the directory containing `watcher.py`.

3. Edit the `path_to_watch` and `gen_folder` variables in the script to point to the correct directories for your CSS and JS files and the generated files, respectively.

4. Run the script:

   ```bash
   python watcher.py
   ```

   The watcher will start monitoring the specified directory for changes.

5. Make changes to your CSS or JS files. When a change is detected, the watcher will automatically run the `bundle.py` script to update the compressed and combined versions of the files.

6. To stop the watcher, press `Ctrl + C` in the terminal.

### Important Notes

- Ensure that both `watcher.py` and `bundle.py` are in the same directory or update the paths accordingly.
- The watcher ignores changes in the `gen` folder to prevent an endless loop caused by changes to the generated files.

---

Feel free to customize this README to better suit your project's structure and any additional details you want to provide.

## Author

Suresh Babu Dhanaraj

- GitHub: [sureshbabudj](https://github.com/sureshbabudj)
- Email: sureshbabudj@gmail.com

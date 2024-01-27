import os
import secrets

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Print the loaded environment variables
print("Loaded environment variables:")
print(f"FLASK_SECRET_KEY: {os.environ.get('FLASK_SECRET_KEY')}")
print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
print(f"FLASK_ENV: {os.environ.get('FLASK_ENV')}")

class Config:
    FLASK_ENV = os.environ.get('FLASK_ENV', "development")
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://admin:root@localhost/ultimate_store")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 20
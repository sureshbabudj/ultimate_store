from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from seed_data import seed_data
import sqlalchemy 
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)
connection_string = app.config['SQLALCHEMY_DATABASE_URI']
engine = sqlalchemy.create_engine(connection_string, pool_pre_ping=True)
app.config['SQLALCHEMY_ENGINE'] = engine

login_manager = LoginManager(app)

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db.init_app(app)
migrate = Migrate(app, db)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# Import and register blueprints
from routes.admin import admin
from routes.shop import shop 
from routes.auth import auth

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(shop, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

if __name__ == "__main__":
    if app.config['FLASK_ENV'] == 'production':
        app.run(debug=False)
    else:
        with app.app_context():
            seed_data()
        app.run(debug=True)

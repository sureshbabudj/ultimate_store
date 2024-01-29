from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

with app.app_context():
    db.create_all()

# Import and register blueprints
from routes.admin import admin
from routes.home import shop

app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(shop, url_prefix='/')

if __name__ == "__main__":
    if app.config['FLASK_ENV'] == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True)


from datetime import datetime
from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db
from flask_assets import Environment, Bundle

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

@app.before_request
def bundle():
    assets = Environment(app)

    # Define CSS and JS bundles
    css_bundle = Bundle(
        'css/bootstrap.css',
        'css/font-awesome.min.css',
        'css/owl.carousel.css',
        'css/responsive.css',
        'css/style.css',
        filters='cssmin',
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
        filters='jsmin',
        output='gen/packed.js'
    )

    # Register the bundles
    assets.register('css_all', css_bundle)
    assets.register('js_all', js_bundle)

if __name__ == "__main__":
    if app.config['FLASK_ENV'] == 'production':
        app.run(debug=False)
    else:
        app.run(debug=True)


#!/bin/bash
set -e

#!/bin/sh
python3 bundle.py

# wait 10 seconds
{ sleep 10; } &

# Export FLASK_APP
export FLASK_APP=app.py

# Flask-Migrate commands for database migration
flask db migrate
flask db upgrade

gunicorn -c gunicorn_config.py app:app
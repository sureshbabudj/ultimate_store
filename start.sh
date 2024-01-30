#!/bin/bash
set -e

#!/bin/sh
python3 bundle.py

# wait 10 seconds
{ sleep 10; } &

flask db stamp head
flask db upgrade

gunicorn -c gunicorn_config.py app:app
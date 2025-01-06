#!/bin/sh

# Change to root directory if scripts folder does not exist in current directory
if [ ! -d scripts ]; then
    cd ..
fi

# Compile translation messages
poetry run python manage.py compilemessages

# Collect static files
poetry run python manage.py collectstatic --no-input

# Migrate database
poetry run python manage.py createcachetable
poetry run python manage.py migrate

# Start Gunicorn/Uvicorn application
poetry run gunicorn application.asgi:application --bind 0.0.0.0:3000 --forwarded-allow-ips '*' --workers 4 --worker-class uvicorn_worker.UvicornWorker --access-logfile '-'

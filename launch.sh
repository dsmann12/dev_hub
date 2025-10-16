#!/bin/sh

# Exit if any command fails
set -e

# Default to 8000 if PORT not set
PORT=${PORT:-8000}

echo "Starting server on port ${PORT}..."

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:${PORT} dev_hub.wsgi:application
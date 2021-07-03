#!/bin/sh

echo "Waiting for DB to be ready..."
sleep 1

echo "Creating migrations..."
python ./manage.py makemigrations

echo "Migrating..."
python ./manage.py migrate

echo "Collecting Django static files..."
python ./manage.py collectstatic --noinput

echo "Starting the server..."
gunicorn server.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

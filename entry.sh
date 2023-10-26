#!/bin/bash
# This is your entrypoint script
# Run Gunicorn in the background
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT &

# Add a sleep to wait for Gunicorn to start (adjust the duration as needed)
sleep 5

# Run your additional commands here
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata db.json

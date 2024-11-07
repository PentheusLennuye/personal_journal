#!/bin/sh
#
# File: /opt/entrypoint.sh
# Set up the .pg files from env
# Initial migrations and, if any tables have changed, make migration
# Start the dev service

./manage.py createsuperuser --no-input 2>/dev/null \
    || echo "superuser ${DJANGO_SUPERUSER_NAME} may already exist"
./manage.py makemigrations
./manage.py migrate

# ./manage.py collectstatic  # Not required for dev, but for staging and prod
./manage.py runserver 0.0.0.0:8000

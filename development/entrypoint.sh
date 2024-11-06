#!/bin/sh
#
# File: /opt/entrypoint.sh
# Set up the .pg files from env
# Initial migrations and, if any tables have changed, make migration
# Start the dev service

cat <<EOPGS >> $HOME/.pg_service.conf
[personal_journal]
host=$DB_HOST
user=$DB_USER
dbname=$DB_NAME
port=$DB_PORT
EOPGS

cat <<EOPGP >> $HOME/.pj_pgpass
$DB_HOST:$DB_PORT:$DB_USER:$DB_PASS
EOPGP

ls -1
./manage.py makemigrations
./manage.py migrate
./manage.py runserver

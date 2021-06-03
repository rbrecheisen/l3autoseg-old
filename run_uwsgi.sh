#!/bin/bash

python manage.py makemigrations
python manage.py migrate auth
python manage.py makemigrations app
python manage.py makemigrations scoring
python manage.py makemigrations segmentation
python manage.py migrate
python manage.py collectstatic --noinput
uwsgi uwsgi.ini

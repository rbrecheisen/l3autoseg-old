#!/usr/bin/env bash

source $HOME/.venv/l3autoseg/bin/activate

export SQLITE3_DIR=/tmp/l3autoseg

python manage.py makemigrations scoring
python manage.py makemigrations segmentation
python manage.py migrate
python manage.py runserver 0.0.0.0:8002

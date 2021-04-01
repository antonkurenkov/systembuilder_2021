#! /bin/bash

python apiproject/manage.py makemigrations --no-input
python apiproject/manage.py migrate --no-input

python apiproject/manage.py createsuperuser --noinput

python apiproject/manage.py runserver 0.0.0.0:8000

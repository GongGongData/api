#!/bin/sh

echo "### Migration ###"
python manage.py migrate

export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=zz3n.dev@gmail.com
export DJANGO_SUPERUSER_PASSWORD=secret

python manage.py createsuperuser --no-input

echo "### Run Server ###"
python manage.py runserver 0.0.0.0:8000

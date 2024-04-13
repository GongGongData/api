#!/bin/sh

echo "### Migration ###"
python manage.py migrate

echo "### Run Server ###"
python manage.py runserver

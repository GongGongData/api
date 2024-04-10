#!/bin/sh
echo "### Docker Build ###"
docker build -t gonggong-db-image .

echo "### Docker Run ###"
docker run -d --name gonggong-db -p 3306:3306 -d gonggong-db-image

echo "### RUN MIGRATE ###"
python3 manage.py migrate
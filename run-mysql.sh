#!/bin/sh
echo "### Docker Build ###"
docker build -t gonggong-db-image .

echo "### Docker Run ###"
docker run -d --name gonggong-db -p 3306:3306 -d gonggong-db-image

cp ./secrets.json ./secrets.json.backup
cp ./secrets-local.json ./secrets.json

echo "### RUN MIGRATE ###"
python3 manage.py migrate
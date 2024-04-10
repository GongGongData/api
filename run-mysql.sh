#!/bin/sh
echo "### Docker Build ###"
docker build -t gonggong-db-image .

echo "### Docker Run in $PWD ###"
mkdir $PWD/datadir
docker run -d --name gonggong-db -v $PWD/datadir:/var/lib/mysql -p 3306:3306 -d gonggong-db-image

cp ./secrets.json ./secrets.json.backup
cp ./secrets-local.json ./secrets.json

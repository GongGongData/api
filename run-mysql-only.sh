#!/bin/sh
echo "### Docker Build in $PWD ###"
docker build -t gonggong-db -f mysql.Dockerfile .

echo "### Setting secrets ###"
cp ./secrets.json ./secrets.json.backup
cp ./secrets-local.json ./secrets.json

echo "### Docker Run in $PWD ###"
mkdir $PWD/datadir

docker run -d --name gonggong-sole-db \
  -v $PWD/datadir:/var/lib/mysql \
  -p 3306:3306 \
  gonggong-db \
  --default-authentication-plugin=mysql_native_password

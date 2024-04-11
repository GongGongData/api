#!/bin/sh

echo "### Setting secrets ###"
cp ./secrets.json ./secrets.json.backup
cp ./secrets-docker.json ./secrets.json

echo "### Docker Compose run in $PWD ###"

mkdir $PWD/datadir
docker-compose -f ./docker-compose.yml up --force-recreate -d --build
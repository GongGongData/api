source .venv/bin/activate

git pull

python3 manage.py collectstatic --clear --no-input

sudo systemctl stop leaflet.service
sudo systemctl start leaflet.service

deactivate

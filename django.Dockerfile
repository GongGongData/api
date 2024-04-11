FROM python:3.9

RUN apt-get -y update
RUN apt-get -y install python3-dev default-libmysqlclient-dev build-essential pkg-config
RUN python -m pip install --upgrade pip

RUN pip install django
RUN pip install pipenv

COPY . /app
WORKDIR /app

COPY ./secrets-docker.json ./secrets.json

RUN pipenv install --dev --system --deploy

CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
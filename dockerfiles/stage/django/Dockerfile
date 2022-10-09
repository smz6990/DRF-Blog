FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY ./requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./core .

RUN mkdir -p /usr/src/app/staticfiles
CMD python3 manage.py check_database && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
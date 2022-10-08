FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./core /app/

RUN mkdir -p /app/staticfiles
CMD python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
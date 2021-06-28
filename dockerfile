FROM tensorflow/tensorflow:latest-gpu
MAINTAINER Ralph Brecheisen <ralph.brecheisen@gmail.com>
COPY requirements.txt /requirements.txt
RUN apt-get -y update && \
    apt-get install -y vim libpq-dev && \
    pip install --upgrade pip && \
    pip install -r /requirements.txt && \
    pip install psycopg2-binary uwsgi gunicorn && \
    mkdir /static && \
    mkdir /src && \
    mkdir /data
WORKDIR /src

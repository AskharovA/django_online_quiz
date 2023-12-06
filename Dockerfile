FROM python:3.11

RUN apt-get update \
    && apt-get install -y gcc libpcre3-dev

ENV PYTHONDONTWRITEBYCODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django_online_quiz

RUN pip install --upgrade pip
COPY requirements.txt /django_online_quiz/
RUN pip install -r requirements.txt
RUN pip install uwsgi
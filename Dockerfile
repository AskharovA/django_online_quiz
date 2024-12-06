FROM python:3.11.9-slim

WORKDIR /django_online_quiz

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y gcc libpcre3-dev

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install gunicorn

FROM python:3.10-slim

WORKDIR app

RUN mkdir -p /app/data/extracted
RUN mkdir -p /app/data/transformed

COPY setup.py .
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .
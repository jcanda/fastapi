FROM python:3.11-slim

WORKDIR /app

# install system dependencies
RUN apt-get update \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY ./app /app

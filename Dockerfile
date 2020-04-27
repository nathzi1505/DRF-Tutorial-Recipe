FROM python:3.7-alpine
MAINTAINER Pritthijit Nath

ENV PYTHONUNBUFFERED 1 # Runs python in unbuffered mode

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app


RUN adduser -D user # Prevents Root Access
USER user
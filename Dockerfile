FROM python:3.8
MAINTAINER "Alireza"
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install -y cron
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /MySite
WORKDIR /MySite
ENV PYTHONPATH "${PYTHONPATH}:/MySite/"
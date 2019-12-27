FROM python:3.7
MAINTAINER Romaric Philogène <rphilogene@qovery.com>

EXPOSE 5000

RUN mkdir -p /app
COPY . /app
WORKDIR /app/src

RUN pip install -r ../requirements.txt
CMD python -u main.py

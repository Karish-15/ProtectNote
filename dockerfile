
FROM python:3.10


ENV PYTHONUNBUFFERED 1


RUN mkdir /protect_note


WORKDIR /protect_note


ADD . /protect_note/


RUN pip install -r requirements.txt
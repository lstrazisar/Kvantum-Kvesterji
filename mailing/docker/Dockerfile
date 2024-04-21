FROM python:3.10-slim-bullseye

RUN mkdir /app
WORKDIR /app

RUN apt-get update

RUN apt-get install -y dos2unix

COPY ./mailing/config .

RUN pip install -r requirements.txt

COPY ./mailing/main.py /app/main.py
COPY ./mailing/gmail /app/gmail

WORKDIR /app/


CMD ["python3", "-u", "main.py"]
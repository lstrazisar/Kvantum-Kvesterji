FROM python:3.10-slim-bullseye

RUN mkdir /app
WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y build-essential gcc
RUN apt-get install -y dos2unix

# dependecy for psycopg2
RUN apt-get install -y libpq-dev

RUN pip3 install --upgrade pip

COPY ./cdc/requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt


COPY ./cdc/helper ./helper
COPY ./cdc/advertisements/main.py ./main.py

CMD ["python", "main.py"] 
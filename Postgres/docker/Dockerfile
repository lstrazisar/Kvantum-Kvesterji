FROM postgres:14-bullseye

# set locale
# ENV LANG sl_SI.UTF-8

# initialize dependency manager
RUN apt-get update && apt-get install -y postgresql-server-dev-14 build-essential
RUN apt-get install -y dos2unix

# install `pg-wal2json`
RUN apt-get install postgresql-14-wal2json
# install `pg_cron`
RUN apt-get install -y postgresql-14-cron

# install python/pip
RUN apt-get install -y python3 python3-pip
RUN pip3 install --no-cache --upgrade pip setuptools

# copy the update scripts
WORKDIR /
COPY Postgres/scripts/00-init-database.sh /docker-entrypoint-initdb.d/00-init-database.sh
RUN dos2unix /docker-entrypoint-initdb.d/00-init-database.sh

RUN mkdir -p /pg/
COPY Postgres/requirements.txt /pg/requirements.txt

# copy the run script
COPY Postgres/run-release /pg/run-release
RUN dos2unix /pg/run-release

# copy Postgres configuration
COPY Postgres/postgresql.conf /etc/postgresql/postgresql.conf
RUN chmod a+w /etc/postgresql/postgresql.conf

RUN chmod 700 /var/lib/postgresql/data
RUN chmod 750 /pg/run-release

WORKDIR /pg/

RUN pip3 install -r requirements.txt

ENTRYPOINT ["./run-release"]
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
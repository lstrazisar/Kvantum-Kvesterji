#!/bin/bash

set -e


psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER $PG_UNAME;
        ALTER USER $PG_UNAME WITH PASSWORD '$PG_PASS';

        CREATE DATABASE $PG_DB;

        GRANT pg_read_all_data TO $PG_UNAME;
        GRANT pg_write_all_data TO $PG_UNAME
EOSQL

# create a table that stores the database information
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$PG_DB" <<-EOSQL
        CREATE TABLE IF NOT EXISTS "system_info" (
            "ignoreMe" SERIAL PRIMARY KEY,
            "databaseVersion" INT NOT NULL
        );

        INSERT INTO "system_info"("databaseVersion") VALUES (0);
EOSQL


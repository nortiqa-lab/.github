#!/bin/bash
# Crea bases de datos adicionales definidas en POSTGRES_MULTIPLE_DATABASES
set -e

create_db() {
    local db=$1
    echo "Creando base de datos: $db"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE "$db";
        GRANT ALL PRIVILEGES ON DATABASE "$db" TO "$POSTGRES_USER";
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
    for db in $(echo "$POSTGRES_MULTIPLE_DATABASES" | tr ',' ' '); do
        if [ "$db" != "$POSTGRES_DB" ] && [ "$db" != "nortiqa" ]; then
            create_db "$db"
        fi
    done
fi

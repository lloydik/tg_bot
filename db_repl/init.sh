#!/bin/bash
service postgresql start && initdb
DATA_PATH=$(psql -U postgres --no-align --quiet --tuples-only --command='SHOW data_directory')
echo $DATA_PATH
pg_ctl stop -D $DATA_PATH
rm -rf /var/lib/postgresql/data
until pg_basebackup -R -h $DB_HOST -D $DATA_PATH -U $DB_REPL_USER -P; do
    echo 'Waiting for primary to connect...'
    sleep 1s
done
echo 'replicated'
pg_ctl start -D $DATA_PATH
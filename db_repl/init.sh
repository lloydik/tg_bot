#!/bin/bash
DATA_PATH=$(psql -U postgres --no-align --quiet --tuples-only --command='SHOW data_directory')
pg_ctl stop -D $DATA_PATH
rm -rf /var/lib/postgresql/data
until pg_basebackup -R -h $DB_HOST -U $DB_REPL_USER -D $DATA_PATH -P; do 
    echo 'Waiting for primary to connect...'
    sleep 1s
done
echo 'replicated'
pg_ctl start -D $DATA_PATH
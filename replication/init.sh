#!/bin/bash
DATA_PATH=$(psql -U postgres --no-align --quiet --tuples-only --command='SHOW data_directory')
echo $DATA_PATH
pg_ctl stop -D $DATA_PATH
rm -rf /var/lib/postgresql/data
until pg_basebackup -R -h db_image -D $DATA_PATH -U replicator -P; do
    echo 'Waiting for primary to connect...'
    sleep 1s
done
echo 'replicated'
pg_ctl start -D $DATA_PATH
# chmod 700 /var/lib/postgresql/data
# postgres

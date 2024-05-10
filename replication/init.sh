#!/bin/bash
service postgresql stop
rm -rf /var/lib/postgresql/16/mycluster/*
until pg_basebackup -R -h db_image -D /var/lib/postgresql/16/mycluster -U replicator; do
    echo 'Waiting for primary to connect...'
    sleep 1s
done
echo 'replicated'
service postgresql start
# chmod 700 /var/lib/postgresql/data
# postgres
FROM postgres:latest
USER postgres

ENV PGUSER=replicator
ENV PGPASSWORD=replicator_password
ENV POSTGRES_PASSWORD=replicator_password
COPY init.sh /docker-entrypoint-initdb.d/
RUN pg_createcluster 16 mycluster
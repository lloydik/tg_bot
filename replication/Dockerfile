FROM postgres:latest

RUN apt update -y && apt upgrade -y && apt install -y postgresql postgresql-contrib sudo systemd iproute2 psmisc
ENV PGUSER=replicator
ENV PGPASSWORD=replicator_password
ENV POSTGRES_PASSWORD=replicator_password

USER postgres

COPY init.sh /docker-entrypoint-initdb.d/
RUN pg_createcluster 16 mycluster
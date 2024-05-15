FROM postgres:latest

RUN apt update -y && apt upgrade -y && apt install -y postgresql postgresql-contrib sudo systemd iproute2 psmisc

ARG DB_REPL_USER
ARG DB_REPL_PASSWORD

ENV PGUSER=${DB_REPL_USER}
ENV PGPASSWORD=${DB_REPL_PASSWORD}
ENV POSTGRES_PASSWORD=${DB_REPL_PASSWORD}

USER postgres

COPY init.sh /docker-entrypoint-initdb.d/init.sh
# RUN pg_createcluster 16 mycluster

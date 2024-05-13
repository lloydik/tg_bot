FROM postgres:latest

ENV POSTGRES_PASSWORD=password
ENV PGPASSWORD=password

COPY 00_init.sql /docker-entrypoint-initdb.d/

# RUN pg_createcluster 16 mycluster

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y openssh-server sudo lsb-release systemd sysstat
RUN apt-get install -y iproute2
RUN rm -rf /var/lib/postgresql/data/*
RUN mkdir /oracle
RUN mkdir /oracle/pg_data
RUN mkdir /oracle/pg_data/archive
RUN chown -R postgres:postgres /oracle/pg_data/archive
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo 'root:admin' | chpasswd
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG sudo postgres
USER postgres
COPY postgresql.conf ./

CMD sudo service ssh restart && \
	service postgresql start && \
	initdb && pg_ctl start && \
#	cp ./postgresql.conf /var/lib/postgresql/data/postgresql.conf && \
	echo "host replication replicator 172.10.1.0/24 trust" >> /var/lib/postgresql/data/pg_hba.conf && \
	echo "host all all 172.10.1.0/24 trust" >> /var/lib/postgresql/data/pg_hba.conf && \
	psql -U postgres -c "CREATE database bot_db;" && \
	psql -U postgres -d bot_db -f /docker-entrypoint-initdb.d/00_init.sql && \
	pg_ctl stop && \
	postgres -c 'listen_addresses=*' -c 'archive_mode=on' -c 'archive_command=cp %p /oracle/pg_data/archive/%f' -c 'max_wal_senders=10' -c 'wal_level=replica' -c 'wal_log_hints=on'
#	tail -F /var/log/postgresql/*.log
EXPOSE 22

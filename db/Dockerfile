FROM postgres:latest

ENV POSTGRES_PASSWORD=password
ENV PGPASSWORD=password

COPY 00_init.sql /docker-entrypoint-initdb.d/

RUN pg_createcluster 16 mycluster

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y openssh-server sudo lsb-release systemd sysstat
RUN apt-get install -y iproute2
RUN mkdir /oracle
RUN mkdir /oracle/pg_data
RUN mkdir /oracle/pg_data/archive
RUN chown -R postgres:postgres /oracle/pg_data/archive
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN echo 'root:admin' | chpasswd
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN usermod -aG sudo postgres
RUN echo "host replication replicator 172.10.1.0/24 trust" >> /etc/postgresql/16/mycluster/pg_hba.conf
RUN echo "host all all 172.10.1.0/24 trust" >> /etc/postgresql/16/mycluster/pg_hba.conf

USER postgres
COPY postgresql.conf /etc/postgresql/16/mycluster/postgresql.conf

CMD service postgresql start && \
	sudo service ssh restart && \
	psql -U postgres -c "CREATE database bot_db;" && \
	psql -U postgres -d bot_db -f /docker-entrypoint-initdb.d/00_init.sql && \
	tail -F /var/log/postgresql/*.log
EXPOSE 22

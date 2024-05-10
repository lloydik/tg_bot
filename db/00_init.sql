CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');

CREATE TABLE IF NOT EXISTS emails (
    ID SERIAL PRIMARY KEY,
    email VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS phones (
    ID SERIAL PRIMARY KEY,
    phone VARCHAR(32)
);
INSERT INTO emails (email) VALUES ('tester@mail.ru'), ('newemail@test.com'), ('vasya@devops.org');
INSERT INTO phones (phone) VALUES ('8 000 000 00 00'), ('+7(999)9999999'), ('+7-123-456-78-90');

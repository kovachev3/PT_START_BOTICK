CREATE USER ${DB_REPL_USER}  WITH REPLICATION ENCRYPTED PASSWORD '${DB_REPL_PASSWORD}';
CREATE DATABASE ${DB_DATABASE};

\c ${DB_DATABASE};

CREATE TABLE IF NOT EXISTS users_email(
    id SERIAL PRIMARY KEY,
    email  VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS users_phone(
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL
);
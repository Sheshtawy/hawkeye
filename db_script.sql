CREATE DATABASE hawkeye_db;

CREATE TABLE clients (
    client_id serial PRIMARY KEY,
    ip_address inet NOT NULL,
    username varchar (50) UNIQUE NOT NULL,
    password varchar (50) NOT NULL,
    port INTEGER,
    email varchar (355) UNIQUE NOT NULL,
    alerts text[][],
    created_on timestamp DEFAULT CURRENT_TIMESTAMP,
    last_connected timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stats (
    stat_id serial PRIMARY KEY,
    client_id integer REFERENCES clients(client_id),
    cpu real,
    memory real,
    uptime real,
    created_on timestamp DEFAULT CURRENT_TIMESTAMP
);




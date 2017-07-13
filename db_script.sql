CREATE TABLE clients (
    client_id serial PRIMARY KEY,
    ip_address inet NOT NULL,
    username varchar (50) UNIQUE NOT NULL,
    password varchar (50) NOT NULL,
    email varchar (355) UNIQUE NOT NULL,
    alerts text[][],
    created_on timestamp NOT NULL,
    last_connected timestamp,
);

CREATE TABLE stats (
    stat_id serial PRIMARY KEY,
    client_id REFERENCES clients(id),
    cpu real,
    memory real,
    uptime real,
    created_on timestamp NOT NULL,
);




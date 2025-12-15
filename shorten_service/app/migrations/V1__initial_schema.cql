CREATE KEYSPACE IF NOT EXISTS url_shortener
WITH REPLICATION = {
    'class': 'NetworkTopologyStrategy',
    'DC1': 3
};

CREATE TABLE IF NOT EXISTS url_shortener.url_map (
    short_code text PRIMARY KEY,
    long_url text,
    created_at timestamp
);
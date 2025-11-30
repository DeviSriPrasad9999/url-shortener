CREATE KEYSPACE IF NOT EXISTS url_shortener
WITH REPLICATION = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
};

CREATE TABLE IF NOT EXISTS url_shortener.url_map (
    short_code text PRIMARY KEY,
    long_url text,
    created_at timestamp
);


CREATE TABLE IF NOT EXISTS url_shortener.schema_migrations (
    version text PRIMARY KEY,
    applied_at timestamp
);

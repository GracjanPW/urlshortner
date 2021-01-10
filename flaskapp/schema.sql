DROP TABLE IF EXISTS urlpair;

CREATE TABLE urlpair (
    short_url TEXT NOT NULL PRIMARY KEY,
    long_url TEXT NOT NULL 
)
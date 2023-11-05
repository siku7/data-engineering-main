drop table if exists locations;


CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    county VARCHAR(255),
    country VARCHAR(255),
    CONSTRAINT unique_location UNIQUE (city, county, country)
);

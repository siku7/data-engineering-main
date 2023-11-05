drop table if exists places;


CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    county VARCHAR(255),
    country VARCHAR(255)
);
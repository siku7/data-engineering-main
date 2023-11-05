-- given_name,family_name,date_of_birth,place_of_birth
drop table if exists people;


CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    given_name VARCHAR(255),
    family_name VARCHAR(255),
    date_of_birth VARCHAR(255),
    place_of_birth VARCHAR(255)
);
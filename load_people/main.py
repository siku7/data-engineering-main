#!/usr/bin/env python

import csv
import json
import sqlalchemy
import os
import psycopg2

#get env variables for DB , it should be in secret manager of some kind in PROD
host = os.environ['HOST']
db = os.environ['DB']
user = os.environ['USER']
password = os.environ['PASSWORD']

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname=db,
    user=user,
    password=password,
    host=host
)
cursor = conn.cursor()

# Function to get location ID based on city name
def get_location_id(city):
    cursor.execute("SELECT id FROM locations WHERE city = %s;", (city,))
    result = cursor.fetchone()
    return result[0] if result else None

# Load people data
with open('data/people.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Get the location ID for the current row's place of birth
        location_id = get_location_id(row['place_of_birth'])
        
        # If a corresponding location is found, insert the person data
        if location_id is not None:
            cursor.execute(
                "INSERT INTO people (given_name, family_name, date_of_birth, place_of_birth_id) VALUES (%s, %s, %s, %s);",
                (row['given_name'], row['family_name'], row['date_of_birth'], location_id)
            )

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

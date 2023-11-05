#!/usr/bin/env python
import csv
import psycopg2
import os

#ENV variables 
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

# Load locations data, making sure duplicates are not loaded 
with open('data/places.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute(
            "INSERT INTO locations (city, county, country) VALUES (%s, %s, %s) ON CONFLICT (city,county,country) DO NOTHING;",
            (row['city'], row['county'], row['country'])
        )

# Commit the transaction
conn.commit()


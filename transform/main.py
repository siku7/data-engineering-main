#!/usr/bin/env python


import csv
import psycopg2
import os
import json

#load db ENV variable, IN PROD it should be in some secret manager
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

query = '''
SELECT
    l.country,
    COUNT(DISTINCT CONCAT(p.given_name, ' ', p.family_name, ' ', p.date_of_birth)) AS people_country_count
FROM
    people p
INNER JOIN locations l ON p.place_of_birth_id = l.id
GROUP BY l.country;
'''
cursor.execute(query=query)

# Fetch all results
results = cursor.fetchall()
results_dict = {country: count for country, count in results}

print(f"result final: {results_dict}")

# Specify the JSON file name
json_file_path = 'data/summary_output.json'

# Write the list of dictionaries to a JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(results_dict, json_file, indent=4)

print(f"Results have been written to {json_file_path}")

# Close the cursor and the connection
cursor.close()
conn.close()



#!/usr/bin/env python

import csv
import json
import sqlalchemy
import os

# connect to the database
DATABASE_URL = os.environ['DATABASE_URL']
engine = sqlalchemy.create_engine(DATABASE_URL)
connection = engine.connect()


# Create a MetaData instance
metadata = sqlalchemy.MetaData()

# reflect the tables
metadata.reflect(bind=engine)

# make an ORM object to refer to the table
# Example = metadata.tables['examples']
Example = sqlalchemy.Table('examples', metadata, autoload=True, autoload_with=engine)

print(f"Writing to database: {DATABASE_URL}")
trans = connection.begin()
# read the CSV data file into the table
with open('data/example.csv') as csv_file:
  reader = csv.reader(csv_file)
  next(reader)
  try:
    for row in reader:
      print(f"row: {row[0]}")
      connection.execute(Example.insert().values(name = row[0]))
    trans.commit()
  except Exception as e:
    trans.rollback()
    print(f"Failiing to write : {e}")
  finally:
    connection.close()

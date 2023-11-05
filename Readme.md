# Test Response

## Code was given as attachment thus instead of forking the original code started it in 'main' branch of this repo and solution in 'test' branch

## Architecture
From architecture perspective given there is a requirement to load ".csv" files for people and places, and there are independent Apps (Dockerized Apps written in Python) that load the .csv file and to be orchestreated with Airflow as shown below

![airflow](https://github.com/filmonhg/data-engineering-main/assets/9483662/a66f89ab-3c91-4ffb-a375-f00d083b5765)


![Screenshot 2023-11-05 at 6 58 57 PM](https://github.com/filmonhg/data-engineering-main/assets/9483662/73f4daaa-8de3-4a07-9d81-b028302e5511)

### CREATE TABLE SCHEMA
db_init: has `01_places_schema.sql` and `02_people_schema.sql` to create the necessary schema in Postgres

1. `01_places_schema.sql`: Making sure there is no duplicate city,county and country as they are used as reference by using city with people table
```sql
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    county VARCHAR(255),
    country VARCHAR(255),
    CONSTRAINT unique_location UNIQUE (city, county, country)
);

                                    Table "public.locations"
 Column  |          Type          | Collation | Nullable |                Default                
---------+------------------------+-----------+----------+---------------------------------------
 id      | integer                |           | not null | nextval('locations_id_seq'::regclass)
 city    | character varying(255) |           |          | 
 county  | character varying(255) |           |          | 
 country | character varying(255) |           |          | 
Indexes:
    "locations_pkey" PRIMARY KEY, btree (id)
    "unique_location" UNIQUE CONSTRAINT, btree (city, county, country)
Referenced by:
    TABLE "people" CONSTRAINT "people_place_of_birth_id_fkey" FOREIGN KEY (place_of_birth_id) REFERENCES locations(id) ON DELETE SET NULL

```
3. `02_people_schema.sql` that uses place_of_birth as foreign key to locations table as follows (Thus normalized) and necessary adjustments in case of deletion to set it to NULL
```sql
CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    given_name VARCHAR(255),
    family_name VARCHAR(255),
    date_of_birth DATE,
    place_of_birth_id INTEGER,
    FOREIGN KEY (place_of_birth_id) REFERENCES locations (id) ON DELETE SET  NULL
);
                                         Table "public.people"
      Column       |          Type          | Collation | Nullable |              Default               
-------------------+------------------------+-----------+----------+------------------------------------
 id                | integer                |           | not null | nextval('people_id_seq'::regclass)
 given_name        | character varying(255) |           |          | 
 family_name       | character varying(255) |           |          | 
 date_of_birth     | date                   |           |          | 
 place_of_birth_id | integer                |           |          | 
Indexes:
    "people_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "people_place_of_birth_id_fkey" FOREIGN KEY (place_of_birth_id) REFERENCES locations(id) ON DELETE SET NULL
```
### LOAD CSV, TRANSFORM and WRITE TO JSON
1. load_people App
   This App loads `people.csv` to postgres table `people` under `codetest` and is dockerzied
2. load_places App
   This App loads `places.csv` to postgres table `locations` under `codetest` and is dockerzied
3. Transform App
   This App reads from "locations" and "people" table to get list of the countries, and a count of how many people were born in that country and is dockerized.
   
### ORCHESTRATION
The application is orchestrated with airflow who manages the flow of execution using `ETL_people_places.py` as `DAG`
```
├── Readme.md
├── docker-compose.yml
├── db_init
│   ├── 01_places_schema.sql
│   ├── 02_people_schema.sql
│   └── 03_example_schema.sql
├── dags
│   ├── ETL_people_places_dag.py
├── data
│   ├── people.csv
│   ├── places.csv
│   ├── sample_output.json
│   └── summary_output.json
├── load_people
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── main.py
│   └── requirements.txt
├── load_places
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── main.py
│   └── requirements.txt
└── transform
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── main.py
│   └── requirements.txt
├── logs
├── db

```


## Sample Data before (in .csv) and after normalization (in Postgres table)
### people.csv
| given_name | family_name | date_of_birth | place_of_birth |
|------------|-------------|---------------|----------------|
| John       | Williams    | 1842-09-30    | Dumfries       |
| Grace      | Jeffery     | 1899-06-14    | Kelso          |
| Sean       | Molnar      | 1982-11-01    | Dromore        |

### people table
```sql
codetest=# select * from people limit 3 ;
 id | given_name | family_name | date_of_birth | place_of_birth_id 
----+------------+-------------+---------------+-------------------
  1 | John       | Williams    | 1842-09-30    |                41
  2 | Grace      | Jeffery     | 1899-06-14    |                67
  3 | Sean       | Molnar      | 1982-11-01    |                38
 ``` 
### places.csv
| city    | county          | country  |
|---------|-----------------|----------|
| Aberdeen| Aberdeenshire   | Scotland |
| Airdrie | Lanarkshire     | Scotland |
| Alloa   | Clackmannanshire| Scotland |
| Annan   | Dumfriesshire   | Scotland |

### locations table
```sql
codetest=# select * from locations limit 4;
 id |   city   |      county      | country  
----+----------+------------------+----------
  1 | Aberdeen | Aberdeenshire    | Scotland
  2 | Airdrie  | Lanarkshire      | Scotland
  3 | Alloa    | Clackmannanshire | Scotland
  4 | Annan    | Dumfriesshire    | Scotland
```
## Execution/Flow and Result
Follow the following instructions when running it:

### PREREQUISITE
customimze absolute path of the `data` folder that will be mounted in each App in `.env` and also version of Airflow which now uses `apache/airflow:latest` but feel free to use any older version as well


```
DATA_DIR='/absolute_path/data'
```

To build images of load,transform Apps as well as Application postgres (with init to create the schema for locations and people) and Airflow (Webserver, scheduler,meta data postgres and db_init to initialize metadata of airflow and schema) 
```
docker-compose up --build -d
```
Default initialized use for Airflow ui : `localhost:8080` will be 
```
user: 'admin'
pass: 'airflow'  
```
1. Postgres schema is created for both `locations` table and `people` table with necessary constraints and normalizations
2. Location table is loaded first given people reference the locations table from location.csv with `load_places` App
3. People table is loaded from people.csv with `load_people` App
4. `transform` App then does the join and executes to get list of the countries, and a count of how many people were born in that country

## RESULT JSON ==> `summary_output.json` as follows 
```json
{
    "Northern Ireland": 1952,
    "Scotland": 8048
}
```
### CLEAN UP
```
docker-compose down -v --remove-orphan

```





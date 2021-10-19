# Sparkify ETL for analytics

This application processes data the Sparkify music streaming startup. 

To support their analytical use cases, the data is organized in a star schema to allow convenient queries over customer interactions. For example, the number of songs played by specific specific users or artists may be directly queried from the `songplays` *fact* table. The queries then may be enriched by joining data from the *dimension* tables `users`, `songs`, `artists` and `time`, for example by filtering by the day of week.

**Fact Table**
- songplays: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

**Dimension Tables**
- users: user_id, first_name, last_name, gender, level
- songs: song_id, title, artist_id, year, duration
- artists: artist_id, name, location, latitude, longitude
- time: start_time, hour, day, week, month, year, weekday

## Structure

The repository is organized as follows:

    ├── logs
    │   └── etl.log             # default logging location
    ├── notebooks             
    │   ├── etl.ipynb           # development notebook
    │   └── test.ipynb          # validation notebook
    ├── poetry.lock             # locked dependencies
    ├── pyproject.toml          # project setup
    └── sparkify_etl            # core package
        ├── __init__.py
        ├── create_tables.py    # script to create schemas
        ├── etl.py              # script to process and insert data
        └── sql_queries.py      # queries used by the scripts

## Setup

For running the ETL examples this project requires both a Python (virtual) environment and a Postgresql database server.

### Set up Postgresql on macOS (optional for local development)

The project assumes a postgres server with a `sparkify` database and `student` user with correct permissions already set up. For developing locally, install postgres and set up the database and user:

```
# install postgresql
brew install postgresql

# start postgres server
brew services start postgres

# create a user "student" that can create dbs
createuser student --createdb

# create database "studentdb" as user student
createdb studentdb --username student
```

### Install the dependencies

The project uses `poetry` to manage dependencies, so make sure you have poetry installed, if not run:

```
pip install poetry
```

To install the package (editable mode by default) with the dependencies (without development dependencies) run:

```
poetry install --no-dev
```

## Run the ETL process

To run the ETL process, first make sure you have completed the [setup](#setup).

1. Create the tables:
```
poetry run python sparkify_etl/create_tables
```

2. Run the ETL:
```
poetry run python sparkify_etl/etl.py
```

3. Validate the results by running the `./notebooks/test.ipynb` notebook.

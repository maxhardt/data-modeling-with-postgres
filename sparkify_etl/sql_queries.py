# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

# songplays - records in log data associated with song plays i.e. records with page NextSong
# songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id SERIAL PRIMARY KEY,
        start_time TIMESTAMP,
        user_id BIGINT,
        level VARCHAR (100),
        song_id VARCHAR (100),
        artist_id VARCHAR (100),
        session_id BIGINT,
        location VARCHAR (100),
        user_agent VARCHAR (150)
    )
""")

# users - users in the app
# user_id, first_name, last_name, gender, level
user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        first_name VARCHAR (100) NOT NULL,
        last_name VARCHAR (100) NOT NULL,
        gender VARCHAR (100) NOT NULL,
        level VARCHAR (100)
    )
""")

# songs - songs in music database
# song_id, title, artist_id, year, duration
song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR (100)  PRIMARY KEY,
        title VARCHAR (100) NOT NULL,
        artist_id VARCHAR (100) NOT NULL,
        year BIGINT NOT NULL,
        duration FLOAT NOT NULL
    )
""")

# artists - artists in music database
# artist_id, name, location, latitude, longitude
artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR (100) PRIMARY KEY,
        name VARCHAR (100) NOT NULL,
        location VARCHAR (100),
        latitude FLOAT,
        longitude FLOAT
    )
""")

# time - timestamps of records in songplays broken down into specific units
# start_time, hour, day, week, month, year, weekday
time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP PRIMARY KEY,
        hour BIGINT NOT NULL,
        day BIGINT NOT NULL,
        week BIGINT NOT NULL,
        month BIGINT NOT NULL,
        year BIGINT NOT NULL,
        weekday BIGINT NOT NULL
    )
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    INSERT INTO users
    (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
    INSERT INTO songs
    (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
    INSERT INTO artists
    ("artist_id", "name", "location", "latitude", "longitude")
    VALUES (%s, %s, %s, %s, %s)
""")

time_table_insert = ("""
    INSERT INTO time
    ("start_time", "hour", "day", "week", "month", "year", "weekday")
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
    SELECT songs.song_id, artists.artist_id FROM songs
    LEFT JOIN artists ON songs.artist_id = artists.artist_id
    WHERE artists.name = %s AND songs.title = %s AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

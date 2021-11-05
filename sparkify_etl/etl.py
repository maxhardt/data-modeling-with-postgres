import argparse
import glob
import logging
import os

import numpy as np
import pandas as pd
import psycopg2

from sparkify_etl.sql_queries import (artist_table_insert, song_select,
                                      song_table_insert, songplay_table_insert,
                                      time_table_insert, user_table_insert)

# let postgres to accept numpy int64 and float64 data types
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
psycopg2.extensions.register_adapter(np.float64, psycopg2._psycopg.AsIs)


def process_song_file(cur, filepath: str, conn):
    """Processes a single song file and inserts the data.

    Args:
        cur (psycopg2 cursor): Postgres cursos object.
        filepath (str): Filepath to song .json file.
        conn (psycopg2 connection): Postgres connection to the database.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    # replace np.nan types with None for postgres
    df = df.replace({np.nan: None})

    # insert song record
    song_columns = ["song_id", "title", "artist_id", "year", "duration"]
    song_data = df[song_columns].iloc[0].values.tolist()
    cur.execute(song_table_insert, song_data)
    conn.commit()

    # insert artist record
    artist_columns = ["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]
    artist_data = df[artist_columns].iloc[0].values
    cur.execute(artist_table_insert, artist_data)
    conn.commit()


def process_log_file(cur, filepath: str, conn):
    """Processes a single log file and inserts the data row-wise.

    Args:
        cur (psycopg2 cursor): Postgres cursos object.
        filepath (str): Filepath to log .json file.
        conn (psycopg2 connection): Postgres connection to the database.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")

    # insert time data records
    time_data = df["ts"].apply(
        lambda x: [x, x.hour, x.day, x.week, x.month, x.year, x.weekday()],
    )
    column_labels = ("timestamp", "hour", "day", "week", "month", "year", "weekday")
    time_df = pd.DataFrame(time_data.to_list(), columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))
        conn.commit()

    # load user table
    user_columns = ["userId", "firstName", "lastName", "gender", "level"]
    user_df = df[user_columns]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
        conn.commit()

    # insert songplay records
    for _, row in df.iterrows():

        # get songid and artistid from song and artist tables
        query_values = row.artist, row.song, row.length
        cur.execute(song_select, query_values)
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            logging.info(f"No entry found for song_id, artist, duration:\n{query_values} ...")
            logging.info("Inserting songplay record without song and artist details...")
            songid, artistid = None, None

        # insert songplay record
        songplay_data = row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, dir: str, func):
    """Inserts all .json files in `dir` to the `sparkify` database using `func` to process.

    Args:
        cur (psycopg2 cursor): Postgres cursos object.
        conn (psycopg2 connection): Postgres connection to the database.
        dir (str): Directory containing all .json files to process.
        func (function): Function to apply to each file.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(dir):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    logging.info('{} files found in {}'.format(num_files, dir))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile, conn)
        logging.info('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, dir='data/song_data', func=process_song_file)
    process_data(cur, conn, dir='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--verbose', default=False, action='store_true',
        help="Enables verbose logging behaviour",
    )

    parser.add_argument(
        '--log-file', type=str, default="logs/etl.log",
        help="Filepath to log to",
    )

    args = parser.parse_args()
    arguments = args.__dict__

    level = logging.INFO if arguments["verbose"] else logging.WARN

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=arguments["log_file"]
    )

    main()

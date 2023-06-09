import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    - Opens .json file as a Series in specified filepath
    - Inserts song records and artist records
    '''
    # open song file. Set typ='series' because single log file contains just one record
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values.tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    - Opens .json file in a specified filepath
    - Enriches the DataFrame with time related columns and inserts them into time table
    - Drops duplicates of user records and filters only users with valid userId
    - Inserts users into user table and songplays into songplays table
    '''
    # open log file with read_json. Set lines=True because source files has /n endings
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # create timestamp column
    df['timestamp'] = pd.to_datetime(df['ts'], unit='ms', origin='unix')
    
    # insert time data records
    df['hour'] = df['timestamp'].dt.hour
    df['day'] = df['timestamp'].dt.day
    df['week'] = df['timestamp'].dt.isocalendar().week
    df['month'] = df['timestamp'].dt.month
    df['year'] = df['timestamp'].dt.year
    df['weekday'] = df['timestamp'].dt.weekday
    
    # select only time columns
    df_time = df[['timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday']]

    for i, row in df_time.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates()
    
    # filter out records with userId == ''
    user_df = user_df[user_df['userId'] != '']

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.timestamp, row.userId, row.level, songid, artistid, \
                        row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    Iterates over .json file and applies processing functions to insert data in bulk
    '''
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    '''
    ETL workflow with all steps executed:
    - Connect to database
    - Create a cursor for SQL statements
    - Process song_data and log_data json files
    - Close connection
    '''
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=admin password=admin")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id SERIAL PRIMARY KEY,
        start_time TIMESTAMP NOT NULL UNIQUE,
        user_id INT NOT NULL,
        level VARCHAR,
        song_id VARCHAR,
        artist_id INT,
        session_id INT,
        location VARCHAR,
        user_agent VARCHAR
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR,
        gender VARCHAR,
        level VARCHAR NOT NULL
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        artist_id VARCHAR NOT NULL,
        year INT NOT NULL,
        duration DECIMAL NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP PRIMARY KEY,
        hour INT NOT NULL,
        day INT NOT NULL,
        week INT NOT NULL,
        month INT NOT NULL,
        year INT NOT NULL,
        weekday INT NOT NULL
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
  INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
  ON CONFLICT (start_time) 
  DO UPDATE SET
    user_id = EXCLUDED.user_id,
    level = EXCLUDED.level,
    song_id = EXCLUDED.song_id,
    artist_id = EXCLUDED.artist_id,
    session_id = EXCLUDED.session_id,
    location = EXCLUDED.location,
    user_agent = EXCLUDED.user_agent;
""")

user_table_insert = ("""
  INSERT INTO users (user_id, first_name, last_name, gender, level)
  VALUES (%s, %s, %s, %s, %s)
  ON CONFLICT (user_id) 
  DO UPDATE SET
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    gender = EXCLUDED.gender,
    level = EXCLUDED.level;
""")

song_table_insert = ("""
  INSERT INTO songs (song_id, title, artist_id, year, duration)
  VALUES (%s, %s, %s, %s, %s)
  ON CONFLICT (song_id) 
  DO UPDATE SET
    title = EXCLUDED.title,
    artist_id = EXCLUDED.artist_id,
    year = EXCLUDED.year,
    duration = EXCLUDED.duration;
""")

artist_table_insert = ("""
  INSERT INTO artists (artist_id, name, location, latitude, longitude)
  VALUES (%s, %s, %s, %s, %s)
  ON CONFLICT (artist_id) 
  DO UPDATE SET
    name = EXCLUDED.name,
    location = EXCLUDED.location,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude;
""")


time_table_insert = ("""
  INSERT INTO time (start_time, hour, day, week, month, year, weekday)
  VALUES (%s, %s, %s, %s, %s, %s, %s)
  ON CONFLICT (start_time) 
  DO UPDATE SET
    hour = EXCLUDED.hour,
    day = EXCLUDED.day,
    week = EXCLUDED.week,
    month = EXCLUDED.month,
    year = EXCLUDED.year,
    weekday = EXCLUDED.weekday;
""")

# FIND SONGS

song_select = ("""
  SELECT
    songs.song_id
    ,artists.artist_id
  FROM songs
  JOIN artists using (artist_id)
  WHERE songs.title = %s
  AND artists.name = %s
  AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
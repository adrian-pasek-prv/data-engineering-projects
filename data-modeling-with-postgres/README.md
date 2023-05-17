# Sparkify Data Model

## Overview:
Sparkify is a music streaming app startup that wants to analyze user activity. Source data is coming in form of JSON files that are not easy to analyze. The goal of the project is to organize data as a Postgres database and model it in a way that will be easy to query for business users. For that purpose, an ETL pipeline is to be used to create a database in star schema.

## How to run Python scripts
- Make sure to have source data [`data/log_data`, `data/song_data`] in the same directory as files [`create_tables.py`, `sql_queries.py`, `etl.py`]
- Your Postgres server is running on `localhost:5432`
- First run `python create_tables.py` in the project directory in the terminal, then run `python etl.py`

## Files

- `create_tables.py` - contains script to setup `sparkifydb` database and create tables
- `sql_queries.py` - contains SQL DDL statments used by Python scripts
- `etl.py` - contains ETL pipeline that processes the data in its entirety

## Database Design
In order to provide an easy way for business users to query data for analysis, a star schema data model was adopted that has a fact table (business mesurements) at its center with adjacent dimension tables (categories that put data into specifc context). This ensures minimal number of joins in order to answer business questions.

ETL pipeline was designed to process the log and song files in the JSON format with the use of Pandas package that enabled necessary transformations and enrichment of the data. The pipeline was created as an executable Python script that will allow for easy integration with other processes.

## Sample Queries
- Who is the most active user on our app?
```
select
	users.first_name
	,users.last_name
	,count(*) as songplays_count
from songplays
join users using(user_id)
group by 1,2
order by songplays_count desc
```
- How many users do we have on "paid" level?
```
select
	count(*) as users_with_paid_level
from users
where level = 'paid'
```
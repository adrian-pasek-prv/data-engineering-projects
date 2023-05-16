from sql_queries import drop_table_queries, create_table_queries
import psycopg2

def create_database():
    '''
    - Creates and connects to sparkifydb
    - Returns a cursor and connection objects
    '''
    
    # Connect to postgres database and setup a cursor plus autocommit
    conn = psycopg2.connect(dbname='postgres',
                            user='admin',
                            password='admin',
                            host='127.0.0.1')
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    # Drop sparkifydb if exists and create it anew
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    # template0 is a pristine template with no encoding involved
    # it allows to specify a chosen encoding
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")
    
    # Close connection to postgres database
    cur.close()
    
    # Open connection to sparkifydb
    conn = psycopg2.connect(dbname='sparkifydb',
                            user='admin',
                            password='admin',
                            host='127.0.0.1')
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    return conn, cur


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list from sql_queries.py
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
        
def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list sql_queries.py. 
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        
def main():
    """
    - Drops (if exists) and Creates the sparkifydb 
    
    - Establishes connection with the sparkifydb and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(conn, cur)
    create_tables(conn, cur)

    conn.close()


if __name__ == "__main__":
    main()
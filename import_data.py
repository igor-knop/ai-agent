import pandas as pd
import psycopg2
from psycopg2 import sql
import sys
from psycopg2.extras import execute_values
from sqlalchemy import values

host = "localhost"
database = "mydb"
password = "mypassword"
user = "myuser"


def connect_to_postgres(host, database, user, password, port = 5432):
    
    try:
        conn = psycopg2.connect(
            host = host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        print(f"Succesfully connected to database {database}")
        return conn
    except Exception as e:
        print(f"Error connecting to database {e}")
        sys.exit(1)
    return conn


def table_exists(conn, table_name):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, (table_name,))
        return cur.fetchone()[0]
        
def push_data_to_postgres(conn, df, table_name):
    with conn.cursor() as cur:
        if not table_exists(conn, table_name):
            columns = [
                sql.SQL("{} TEXT").format(sql.Identifier(col))
                for col in df.columns
            ]
            query = sql.SQL("""
            CREATE TABLE {} (
                {}
            )
            """).format(
                sql.Identifier(table_name),
                sql.SQL(", ").join(columns)
            )
            cur.execute(query)
        
        columns = sql.SQL(", ").join(
            sql.Identifier(col) for col in df.columns
        )
        insert_query = sql.SQL(
            "INSERT INTO {} ({}) VALUES %s"
        ).format(
            sql.Identifier(table_name),
            columns
        )
        values = [tuple(row) for row in df.values]
        execute_values(cur, insert_query, values)
        
    conn.commit()

def display_table_data(conn, table_name, limit=None):
    if not table_exists(conn, table_name):
        print(f"Table '{table_name}' does not exist.")
        return None
    
    with conn.cursor() as cur:
        query = sql.SQL("SELECT * FROM {}").format(
            sql.Identifier(table_name)
        )
        if limit is not None:
            query = sql.SQL("{} LIMIT %s").format(query)
            cur.execute(query, (limit,))
        else:
            cur.execute(query)
            
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        
    return df

def drop_table(conn, table_name):
    """Drop a table if it exists."""
    with conn.cursor() as cur:
        query = sql.SQL("DROP TABLE IF EXISTS {}").format(
            sql.Identifier(table_name)
        )
        cur.execute(query)
    conn.commit()

def main():
    DB_CONFIG = {
        "host" : "localhost",
        "database" : "mydb",
        "password" : "mypassword",
        "user" : "myuser"
    }
    
    try:
        conn = connect_to_postgres(**DB_CONFIG)
        df = pd.read_excel("production_data.xlsx")
        drop_table(conn, "production_data")
        push_data_to_postgres(conn, df, "production_data")
        df = display_table_data(conn, "production_data")
        print(df)
    except Exception as e:
        print(f"Error executing the script {e}")
    finally:
        conn.close()
    
if __name__ == "__main__":
    main()
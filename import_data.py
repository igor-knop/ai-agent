import pandas as pd
import psycopg2
from psycopg2 import sql
import sys

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



def main():
    DB_CONFIG = {
        "host" : "localhost",
        "database" : "mydb",
        "password" : "mypassword",
        "user" : "myuser"
    }
    
    try:
        connect_to_postgres(**DB_CONFIG)
    except Exception as e:
        print("Error executing the script {e}")

if __name__ == "__main__":
    main()
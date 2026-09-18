import sqlite3
import sys 
from pathlib import Path 
import pandas as pd 
from dotenv import load_dotenv 
import os 

load_dotenv()

DB_path = Path(os.getenv("DB_PATH"))

def main():
    if len(sys.argv) !=2:
        print("Usage: python src/run_sql.py sql/query.sql")
        sys.exit(1)


    sql_path = Path(sys.argv[1])

    query = sql_path.read_text()

    connection = sqlite3.connect(DB_path)

    result = pd.read_sql_query(
        query,
        connection
    )

    connection.close()
    print(result.to_string(index=False))

if __name__ == '__main__':
    main()
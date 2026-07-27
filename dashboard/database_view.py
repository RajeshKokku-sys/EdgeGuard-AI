import sqlite3
import pandas as pd

def load_events():

    conn = sqlite3.connect("database/edgeguard.db")

    df = pd.read_sql_query(
        "SELECT * FROM events ORDER BY id DESC",
        conn
    )

    conn.close()

    return df
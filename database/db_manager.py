import sqlite3


class DatabaseManager:

    def __init__(
        self,
        db_name="database/edgeguard.db"
    ):

        self.connection = sqlite3.connect(
            db_name
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS events(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            camera TEXT,

            event_type TEXT,

            confidence REAL,

            timestamp TEXT

        )

        """)

        self.connection.commit()

    def insert_event(self, event):

        self.cursor.execute("""

        INSERT INTO events(

            camera,

            event_type,

            confidence,

            timestamp

        )

        VALUES(?,?,?,?)

        """,

        (

            event["camera"],

            event["event_type"],

            event["confidence"],

            str(event["timestamp"])

        )

        )

        self.connection.commit()

    def close(self):

        self.connection.close()
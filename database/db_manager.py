import sqlite3


class DatabaseManager:

    def __init__(
        self,
        db_name="database/edgeguard.db"
    ):

        self.db_name = db_name

        self.connection = sqlite3.connect(
            self.db_name
        )

        self.cursor = self.connection.cursor()

        self.create_tables()


    # ---------------------------------------
    # Create Database Tables
    # ---------------------------------------

    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS events(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            camera TEXT,

            track_id INTEGER,

            zone_name TEXT,

            event_type TEXT,

            confidence REAL,

            timestamp TEXT

        )

        """)


        self.connection.commit()



    # ---------------------------------------
    # Insert Security Event
    # ---------------------------------------

    def insert_event(
        self,
        event
    ):

        self.cursor.execute("""

        INSERT INTO events(

            camera,

            track_id,

            zone_name,

            event_type,

            confidence,

            timestamp

        )

        VALUES(?,?,?,?,?,?)

        """,

        (

            event["camera"],

            event["track_id"],

            event["zone_name"],

            event["event_type"],

            event["confidence"],

            str(event["timestamp"])

        )

        )


        self.connection.commit()



    # ---------------------------------------
    # Retrieve Events
    # Used by Dashboard
    # ---------------------------------------

    def get_events(self):

        query = """

        SELECT

            id,

            camera,

            track_id,

            event_type,

            zone_name,

            confidence,

            timestamp


        FROM events


        ORDER BY timestamp DESC

        """


        self.cursor.execute(query)


        events = self.cursor.fetchall()


        return events



    # ---------------------------------------
    # Get Latest Events
    # Optional Dashboard Feature
    # ---------------------------------------

    def get_latest_events(
        self,
        limit=10
    ):

        query = """

        SELECT

            id,

            camera,

            track_id,

            event_type,

            zone_name,

            confidence,

            timestamp


        FROM events


        ORDER BY id DESC


        LIMIT ?

        """


        self.cursor.execute(
            query,
            (limit,)
        )


        return self.cursor.fetchall()



    # ---------------------------------------
    # Close Database
    # ---------------------------------------

    def close(self):

        self.connection.close()
import sqlite3


class DatabaseManager:


    def __init__(
        self,
        db_name="database/edgeguard.db"
    ):

        self.connection = sqlite3.connect(
            db_name,
            check_same_thread=False
        )

        self.cursor = self.connection.cursor()

        self.create_tables()


    # ------------------------------------
    # Create Tables
    # ------------------------------------

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


        self.cursor.execute("""
        
        CREATE TABLE IF NOT EXISTS evidence(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_id INTEGER,

            image_path TEXT,

            video_path TEXT,

            created_time TEXT,

            FOREIGN KEY(event_id)
            REFERENCES events(id)

        )

        """)


        self.connection.commit()



    # ------------------------------------
    # Insert Event
    # ------------------------------------

    def insert_event(self,event):


        self.cursor.execute(
        """

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

        ))


        self.connection.commit()


        return self.cursor.lastrowid



    # ------------------------------------
    # Insert Evidence
    # ------------------------------------

    def insert_evidence(

        self,

        event_id,

        image_path,

        video_path

    ):


        self.cursor.execute(
        """

        INSERT INTO evidence(

            event_id,

            image_path,

            video_path,

            created_time

        )

        VALUES(?,?,?,datetime('now'))

        """,

        (

            event_id,

            image_path,

            video_path

        ))


        self.connection.commit()



    # ------------------------------------
    # Dashboard Query
    # ------------------------------------

    def get_events_with_evidence(self):


        query = """

        SELECT

        events.id,

        events.camera,

        events.track_id,

        events.zone_name,

        events.event_type,

        events.confidence,

        events.timestamp,

        evidence.image_path,

        evidence.video_path


        FROM events


        LEFT JOIN evidence


        ON events.id = evidence.event_id


        ORDER BY events.timestamp DESC


        """


        result = self.cursor.execute(
            query
        ).fetchall()


        return result



    # ------------------------------------
    # Close DB
    # ------------------------------------

    def close(self):

        self.connection.close()
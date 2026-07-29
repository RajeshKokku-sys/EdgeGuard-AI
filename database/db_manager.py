import sqlite3
import pickle

from config.settings import Settings


class DatabaseManager:
    """
    EdgeGuard AI Database Manager

    Handles:
    - Employees
    - Events
    - Evidence
    """

    def __init__(self):

        self.connection = sqlite3.connect(
            Settings.DATABASE_PATH,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

    # =====================================================
    # CREATE TABLES
    # =====================================================

    def create_tables(self):

        # -------------------------
        # Employee Table
        # -------------------------

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS employees(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            employee_id TEXT UNIQUE,

            name TEXT,

            department TEXT,

            designation TEXT,

            embedding BLOB,

            created_time TEXT DEFAULT CURRENT_TIMESTAMP

        )

        """)

        # -------------------------
        # Event Table
        # -------------------------

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS events(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            camera TEXT,

            track_id INTEGER,

            person_name TEXT,

            authentication TEXT,

            zone_name TEXT,

            event_type TEXT,

            confidence REAL,

            timestamp TEXT

        )

        """)

        # -------------------------
        # Evidence Table
        # -------------------------

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS evidence(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            event_id INTEGER,

            image_path TEXT,

            video_path TEXT,

            created_time TEXT DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(event_id)
            REFERENCES events(id)

        )

        """)

        self.connection.commit()

    # =====================================================
    # EMPLOYEE METHODS
    # =====================================================

    def add_employee(

        self,

        employee_id,

        name,

        department,

        designation,

        embedding

    ):

        embedding_blob = pickle.dumps(
            embedding
        )

        self.cursor.execute("""

        INSERT INTO employees(

            employee_id,

            name,

            department,

            designation,

            embedding

        )

        VALUES(?,?,?,?,?)

        """,

        (

            employee_id,

            name,

            department,

            designation,

            embedding_blob

        ))

        self.connection.commit()

    def get_all_employees(self):

        result = self.cursor.execute("""

        SELECT *

        FROM employees

        ORDER BY name

        """)

        return result.fetchall()

    def get_employee_embeddings(self):

        result = self.cursor.execute("""

        SELECT

        employee_id,

        name,

        department,

        designation,

        embedding

        FROM employees

        """)

        employees = []

        for row in result.fetchall():

            employees.append({

                "employee_id": row["employee_id"],

                "name": row["name"],

                "department": row["department"],

                "designation": row["designation"],

                "embedding": pickle.loads(
                    row["embedding"]
                )

            })

        return employees

    # =====================================================
    # EVENT METHODS
    # =====================================================

    def insert_event(self, event):

        self.cursor.execute("""

        INSERT INTO events(

            camera,

            track_id,

            person_name,

            authentication,

            zone_name,

            event_type,

            confidence,

            timestamp

        )

        VALUES(?,?,?,?,?,?,?,?)

        """,

        (

            event["camera"],

            event["track_id"],

            event["person_name"],

            event["authentication"],

            event["zone_name"],

            event["event_type"],

            event["confidence"],

            str(event["timestamp"])

        ))

        self.connection.commit()

        return self.cursor.lastrowid

    def get_events(self):

        result = self.cursor.execute("""

        SELECT *

        FROM events

        ORDER BY timestamp DESC

        """)

        return result.fetchall()

    # =====================================================
    # EVIDENCE METHODS
    # =====================================================

    def insert_evidence(

        self,

        event_id,

        image_path,

        video_path

    ):

        self.cursor.execute("""

        INSERT INTO evidence(

            event_id,

            image_path,

            video_path

        )

        VALUES(?,?,?)

        """,

        (

            event_id,

            image_path,

            video_path

        ))

        self.connection.commit()

    # =====================================================
    # DASHBOARD QUERY
    # =====================================================

    def get_events_with_evidence(self):

        result = self.cursor.execute("""

        SELECT

            events.id,

            events.camera,

            events.track_id,

            events.person_name,

            events.authentication,

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

        """)

        return result.fetchall()

    # =====================================================
    # DASHBOARD STATISTICS
    # =====================================================

    def get_dashboard_statistics(self):

        stats = {}

        stats["employees"] = self.cursor.execute(

            "SELECT COUNT(*) FROM employees"

        ).fetchone()[0]

        stats["events"] = self.cursor.execute(

            "SELECT COUNT(*) FROM events"

        ).fetchone()[0]

        stats["intrusions"] = self.cursor.execute("""

            SELECT COUNT(*)

            FROM events

            WHERE event_type='ZONE_INTRUSION'

        """).fetchone()[0]

        stats["unknown_people"] = self.cursor.execute("""

            SELECT COUNT(*)

            FROM events

            WHERE authentication='UNAUTHORIZED'

        """).fetchone()[0]

        return stats

    # =====================================================
    # DELETE METHODS
    # =====================================================

    def delete_event(self, event_id):

        self.cursor.execute(

            "DELETE FROM evidence WHERE event_id=?",

            (event_id,)

        )

        self.cursor.execute(

            "DELETE FROM events WHERE id=?",

            (event_id,)

        )

        self.connection.commit()

    # =====================================================
    # CLOSE DATABASE
    # =====================================================

    def close(self):

        self.connection.close()
from database.db_manager import DatabaseManager
from datetime import datetime

db = DatabaseManager()

event = {
    "camera": "Main Entrance",
    "track_id": 1,
    "person_name": "Unknown",
    "authentication": "UNAUTHORIZED",
    "zone_name": "Vault",
    "event_type": "ZONE_INTRUSION",
    "confidence": 0.97,
    "timestamp": datetime.now()
}

event_id = db.insert_event(event)

db.insert_evidence(
    event_id,
    "evidence/images/event_1.jpg",
    "evidence/videos/event_1.mp4"
)

print("Event ID:", event_id)

print("\nDashboard Data")

for row in db.get_events_with_evidence():
    print(dict(row))

print("\nStatistics")

print(db.get_dashboard_statistics())

db.close()
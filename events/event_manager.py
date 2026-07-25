from datetime import datetime


class EventManager:
    def create_event(
        self,
        camera_name,
        confidence,
        track_id,
        event_type="PERSON_DETECTED"
    ):
        event = {
            "camera": camera_name,
            "track_id": track_id,
            "event_type": event_type,
            "confidence": confidence,
            "timestamp": datetime.now()
        }

        return event
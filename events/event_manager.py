from datetime import datetime


class EventManager:

    def create_event(
        self,
        camera_name,
        confidence,
        track_id,
        event_type="PERSON_DETECTED",
        zone_name=None
    ):

        event = {
            "camera": camera_name,
            "track_id": track_id,
            "event_type": event_type,
            "zone_name": zone_name,
            "confidence": confidence,
            "timestamp": datetime.now()
        }

        return event
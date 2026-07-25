from datetime import datetime


class EventManager:
    """
    Creates standardized security events.
    """

    def create_event(
        self,
        camera_name,
        confidence,
        event_type="PERSON_DETECTED"
    ):

        event = {
            "camera": camera_name,
            "event_type": event_type,
            "confidence": confidence,
            "timestamp": datetime.now()
        }

        return event
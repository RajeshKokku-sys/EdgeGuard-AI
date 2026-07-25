from datetime import datetime, timedelta


class EventDeduplicationManager:
    """
    Prevents duplicate events for the same tracked person.
    """

    def __init__(self, cooldown_seconds=10):
        self.cooldown = timedelta(seconds=cooldown_seconds)
        self.last_seen = {}

    def should_create_event(self, track_id):
        now = datetime.now()

        if track_id not in self.last_seen:
            self.last_seen[track_id] = now
            return True

        elapsed = now - self.last_seen[track_id]

        if elapsed > self.cooldown:
            self.last_seen[track_id] = now
            return True

        return False
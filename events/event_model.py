from datetime import datetime
from dataclasses import dataclass


@dataclass
class SecurityEvent:
    """
    Standard Event Object
    """

    camera: str

    track_id: int

    person_name: str

    authentication: str

    zone_name: str

    event_type: str

    confidence: float

    severity: str

    timestamp: datetime = datetime.now()


    def to_dict(self):

        return {

            "camera":
                self.camera,

            "track_id":
                self.track_id,

            "person_name":
                self.person_name,

            "authentication":
                self.authentication,

            "zone_name":
                self.zone_name,

            "event_type":
                self.event_type,

            "confidence":
                self.confidence,

            "severity":
                self.severity,

            "timestamp":
                self.timestamp

        }
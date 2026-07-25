from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SecurityEvent:
    camera_id: str
    event_type: str
    confidence: float
    created_at: datetime

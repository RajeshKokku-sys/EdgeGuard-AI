from dataclasses import dataclass


@dataclass
class EvidenceTask:
    """
    Represents an evidence generation job
    """

    frame: object

    frames: list

    event: object

    event_id: int
from dataclasses import dataclass


@dataclass
class CameraConfig:


    id: str

    name: str

    source: object

    location: str

    enabled: bool
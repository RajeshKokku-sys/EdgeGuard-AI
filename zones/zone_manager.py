import json
from pathlib import Path


class ZoneManager:
    def __init__(self, zones_file: str | Path):
        self.zones_file = Path(zones_file)

    def load_zones(self) -> dict:
        with self.zones_file.open("r", encoding="utf-8") as file:
            return json.load(file)

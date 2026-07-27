import json
import cv2
import numpy as np


class ZoneManager:

    def __init__(self, zone_file="zones/zones.json"):

        with open(zone_file, "r") as f:
            self.zones = json.load(f)["zones"]

    def draw_zones(self, frame):

        for zone in self.zones:

            pts = np.array(zone["polygon"], np.int32)

            cv2.polylines(
                frame,
                [pts],
                True,
                (0,255,255),
                2
            )

            x, y = pts[0]

            cv2.putText(
                frame,
                zone["name"],
                (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,255),
                2
            )

        return frame

    def check_intrusion(self, x, y):

        for zone in self.zones:

            polygon = np.array(
                zone["polygon"],
                np.int32
            )

            inside = cv2.pointPolygonTest(
                polygon,
                (int(x), int(y)),
                False
            )

            if inside >= 0:

                return True, zone["name"]

        return False, None
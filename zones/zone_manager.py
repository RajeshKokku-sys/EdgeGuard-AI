import json
import cv2
import numpy as np

from config.settings import Settings


class ZoneManager:
    """
    Handles restricted zone detection.

    Uses Bottom Center Point
    instead of Bounding Box Center.

    Pipeline:

    YOLO bbox
          |
          |
    Bottom Center Point
          |
          |
    Polygon Test
          |
          |
    Intrusion Decision
    """

    def __init__(self):

        self.zone_file = Settings.ZONE_FILE

        self.zones = self.load_zones()


    # =================================================
    # Load Zones
    # =================================================

    def load_zones(self):

        with open(
            self.zone_file,
            "r"
        ) as file:

            return json.load(file)



    # =================================================
    # Get Camera Zones
    # =================================================

    def get_camera_zones(
        self,
        camera_name
    ):

        if camera_name in self.zones:

            return self.zones[camera_name]["zones"]


        return []



    # =================================================
    # Calculate Foot Point
    # =================================================

    def get_bottom_center_point(
        self,
        bbox
    ):

        """
        Calculates the point where
        person's feet touch ground.

        bbox:

        x1,y1,x2,y2

        """

        x1, y1, x2, y2 = bbox


        foot_x = int(
            (x1 + x2) / 2
        )


        foot_y = int(y2)


        return (
            foot_x,
            foot_y
        )



    # =================================================
    # Polygon Conversion
    # =================================================

    def create_polygon(
        self,
        points
    ):

        return np.array(
            points,
            dtype=np.int32
        )



    # =================================================
    # Point Inside Zone Test
    # =================================================

    def is_inside_zone(

        self,

        bbox,

        zone_points

    ):

        foot_point = self.get_bottom_center_point(
            bbox
        )


        polygon = self.create_polygon(
            zone_points
        )


        result = cv2.pointPolygonTest(

            polygon,

            foot_point,

            False

        )


        return result >= 0



    # =================================================
    # Intrusion Detection
    # =================================================

    def check_intrusion(

        self,

        camera_name,

        bbox

    ):

        zones = self.get_camera_zones(
            camera_name
        )


        for zone in zones:


            inside = self.is_inside_zone(

                bbox,

                zone["points"]

            )


            if inside:


                return {


                    "intrusion": True,


                    "zone_name":
                        zone["name"],


                    "zone_type":
                        zone["type"],


                    "foot_point":
                        self.get_bottom_center_point(
                            bbox
                        )

                }



        return {


            "intrusion": False,


            "zone_name": None,


            "zone_type": None,


            "foot_point":
                self.get_bottom_center_point(
                    bbox
                )

        }



    # =================================================
    # Draw Zones
    # =================================================

    def draw_zones(

        self,

        frame,

        camera_name

    ):

        zones = self.get_camera_zones(
            camera_name
        )


        for zone in zones:


            polygon = self.create_polygon(

                zone["points"]

            )


            cv2.polylines(

                frame,

                [polygon],

                True,

                (0,0,255),

                2

            )


            x,y = zone["points"][0]


            cv2.putText(

                frame,

                zone["name"],

                (x,y-10),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                (0,0,255),

                2

            )


        return frame



    # =================================================
    # Draw Foot Point
    # =================================================

    def draw_person_position(

        self,

        frame,

        bbox

    ):


        foot_point = self.get_bottom_center_point(
            bbox
        )


        cv2.circle(

            frame,

            foot_point,

            6,

            (0,255,0),

            -1

        )


        return frame
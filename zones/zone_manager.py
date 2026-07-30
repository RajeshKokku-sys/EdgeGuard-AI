import json
import cv2
import numpy as np



class ZoneManager:


    def __init__(self, config_file):


        with open(config_file,"r") as f:

            data = json.load(f)


        self.zones = data["zones"]



    def point_inside_zone(
        self,
        point,
        zone_points
    ):


        polygon = np.array(
            zone_points,
            np.int32
        )


        result = cv2.pointPolygonTest(

            polygon,

            point,

            False

        )


        return result >= 0



    def check_zone(
        self,
        point
    ):


        detected_zone = None


        intrusion = False



        for zone in self.zones:


            inside = self.point_inside_zone(

                point,

                zone["points"]

            )


            if inside:


                detected_zone = zone["name"]


                if zone["type"] == "restricted":

                    intrusion = True



        return {

            "zone":
                detected_zone,

            "intrusion":
                intrusion

        }



    def draw_zones(
        self,
        frame
    ):


        for zone in self.zones:


            points = np.array(

                zone["points"],

                np.int32

            )


            color = (
                0,0,255
            ) if zone["type"]=="restricted" else (

                0,255,0

            )


            cv2.polylines(

                frame,

                [points],

                True,

                color,

                2

            )


            cv2.putText(

                frame,

                zone["name"],

                tuple(points[0]),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                color,

                2

            )


        return frame
from tracking.tracker import PersonTracker

from zones.zone_manager import ZoneManager

import os

import cv2



class AIPipeline:


    def __init__(self):


        self.tracker = PersonTracker()


        self.zone_manager = ZoneManager(

            os.path.join(

                "zones",

                "zones.json"

            )

        )



    def process(self, frame):


        results, tracked_people = self.tracker.track(
            frame
        )



        result = results[0]



        annotated_frame = result.plot()



        # Draw zones

        annotated_frame = self.zone_manager.draw_zones(

            annotated_frame

        )



        people=[]



        for person in tracked_people:


            x1,y1,x2,y2 = person["bbox"]



            # Bottom center

            center_x = int(
                (x1+x2)/2
            )

            center_y = int(
                y2
            )



            zone_result = self.zone_manager.check_zone(

                (
                    center_x,

                    center_y

                )

            )



            person["zone"] = zone_result["zone"]

            person["intrusion"] = zone_result["intrusion"]



            # Draw feet point

            cv2.circle(

                annotated_frame,

                (
                    center_x,

                    center_y

                ),

                5,

                (0,0,255),

                -1

            )



            people.append(person)



        return {


            "frame":

                annotated_frame,


            "people":

                people

        }
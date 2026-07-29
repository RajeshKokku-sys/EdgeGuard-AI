from tracking.tracker import PersonTracker


class AIPipeline:
    """
    Complete AI Processing Pipeline

    Camera Frame
          |
          ▼
       YOLO
          |
          ▼
      ByteTrack
          |
          ▼
   Face Recognition
          |
          ▼
  Structured Person Data
    """


    def __init__(self):

        self.tracker = PersonTracker()



    def process(self, frame):


        # =====================================
        # Detection + Tracking + Face Recognition
        # =====================================

        results, tracked_people = self.tracker.track(
            frame
        )



        # =====================================
        # YOLO Result Handling
        # =====================================

        if isinstance(results, list):

            result = results[0]

        else:

            result = results



        # Draw YOLO bounding boxes

        annotated_frame = result.plot()



        # =====================================
        # Prepare AI Response
        # =====================================

        people = []



        for person in tracked_people:


            people.append(

                {

                    "track_id":
                        person["track_id"],


                    "confidence":
                        person["confidence"],


                    "bbox":
                        person["bbox"],


                    "identity":
                        person["identity"]

                }

            )



        return {


            "frame":

                annotated_frame,


            "people":

                people

        }
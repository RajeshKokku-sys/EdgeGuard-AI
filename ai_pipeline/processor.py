from ai_pipeline.pipeline import AIPipeline



class FrameProcessor:


    def __init__(self):

        self.pipeline = AIPipeline()



    def process_camera_frame(
        self,
        camera_name,
        frame
    ):


        result = self.pipeline.process(
            frame
        )


        return {


            "camera":

                camera_name,


            "frame":

                result["frame"],


            "people":

                result["people"]

        }
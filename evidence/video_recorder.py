import cv2
import os

from config.settings import Settings


class VideoRecorder:


    def __init__(self):

        self.fps = Settings.VIDEO_FPS



    def save_video(

        self,

        frames,

        filename

    ):


        if len(frames)==0:

            return None



        path = os.path.join(

            Settings.VIDEO_FOLDER,

            filename

        )


        height, width = frames[0][1].shape[:2]


        writer = cv2.VideoWriter(

            path,

            cv2.VideoWriter_fourcc(
                *"mp4v"
            ),

            self.fps,

            (
                width,
                height
            )

        )


        for _,frame in frames:

            writer.write(frame)


        writer.release()


        return path
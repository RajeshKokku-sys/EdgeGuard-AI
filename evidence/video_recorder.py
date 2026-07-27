import cv2
import time


class VideoRecorder:


    def __init__(
        self,
        fps=20,
        duration=30
    ):

        self.fps=fps

        self.duration=duration



    def save_video(
        self,
        frames,
        filename
    ):


        if len(frames)==0:

            return None


        height,width,_ = frames[0].shape


        writer=cv2.VideoWriter(

            filename,

            cv2.VideoWriter_fourcc(
                *"mp4v"
            ),

            self.fps,

            (width,height)

        )


        for frame in frames:

            writer.write(frame)


        writer.release()


        return filename
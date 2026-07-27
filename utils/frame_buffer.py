from collections import deque


class FrameBuffer:


    def __init__(
        self,
        size=200
    ):

        self.frames = deque(
            maxlen=size
        )


    def add(self,frame):

        self.frames.append(
            frame.copy()
        )


    def get_frames(self):

        return list(
            self.frames
        )
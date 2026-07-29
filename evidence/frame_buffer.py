from collections import deque
import time


class FrameBuffer:

    """
    Stores recent frames
    for pre-event recording
    """

    def __init__(
        self,
        max_frames=200
    ):

        self.buffer = deque(
            maxlen=max_frames
        )


    def add_frame(
        self,
        frame
    ):

        self.buffer.append(
            (
                time.time(),
                frame.copy()
            )
        )


    def get_frames(self):

        return list(
            self.buffer
        )


    def clear(self):

        self.buffer.clear()
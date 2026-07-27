import cv2
import os
from datetime import datetime


class EvidenceManager:


    def __init__(self):

        self.image_folder = (
            "evidence/images"
        )

        self.video_folder = (
            "evidence/videos"
        )


        os.makedirs(
            self.image_folder,
            exist_ok=True
        )


        os.makedirs(
            self.video_folder,
            exist_ok=True
        )


    def save_snapshot(
        self,
        frame,
        event_id
    ):


        filename = (
            f"event_{event_id}_"
            +
            datetime.now()
            .strftime("%Y%m%d_%H%M%S")
            +
            ".jpg"
        )


        path = os.path.join(

            self.image_folder,

            filename

        )


        cv2.imwrite(
            path,
            frame
        )


        return path
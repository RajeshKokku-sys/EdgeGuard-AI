import cv2

import os

from datetime import datetime


class EvidenceManager:

    def __init__(self):

        self.output_folder = "evidence/images"

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    def save_snapshot(
        self,
        frame,
        event
    ):

        filename = datetime.now().strftime(
            "%Y%m%d_%H%M%S.jpg"
        )

        path = os.path.join(
            self.output_folder,
            filename
        )

        cv2.imwrite(
            path,
            frame
        )

        return path
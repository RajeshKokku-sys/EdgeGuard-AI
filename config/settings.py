import os
from dotenv import load_dotenv


load_dotenv()


class Settings:


    CAMERA_SOURCE = int(
        os.getenv(
            "CAMERA_SOURCE",
            0
        )
    )


    CONFIDENCE_THRESHOLD = float(
        os.getenv(
            "CONFIDENCE_THRESHOLD",
            0.5
        )
    )


    MODEL_PATH = os.getenv(
        "MODEL_PATH",
        "yolov8n.pt"
    )
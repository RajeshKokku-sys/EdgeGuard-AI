from ultralytics import YOLO

from config.settings import Settings


class PersonDetector:
    """
    Wrapper around the YOLO model.
    Responsible only for loading the model and
    performing inference.
    """

    def __init__(self, model_path=None):

        if model_path is None:
            model_path = Settings.MODEL_PATH

        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model(
            frame,
            verbose=False
        )

        return results
class PersonTracker:
    """
    Wrapper around Ultralytics ByteTrack.
    """

    def __init__(self, detector):
        self.detector = detector

    def track(self, frame):
        results = self.detector.model.track(
            source=frame,
            persist=True,
            tracker="bytetrack.yaml",
            verbose=False
        )

        return results
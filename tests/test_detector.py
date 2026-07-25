import unittest
from unittest.mock import patch

from detection.detector import Detection, PersonDetector


class FakeValue:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, index):
        return self.value


class FakeBox:
    def __init__(self, class_id, confidence, xyxy):
        self.cls = FakeValue(class_id)
        self.conf = FakeValue(confidence)
        self.xyxy = [xyxy]


class FakeResult:
    def __init__(self, boxes):
        self.boxes = boxes


def fake_yolo(model_path):
    class FakeModel:
        def __call__(self, frame):
            return [
                FakeResult(
                    [
                        FakeBox(0, 0.9, [10, 20, 30, 40]),
                        FakeBox(2, 0.95, [1, 2, 3, 4]),
                        FakeBox(0, 0.2, [5, 6, 7, 8]),
                    ]
                )
            ]

    return FakeModel()


class PersonDetectorTest(unittest.TestCase):
    def test_detect_people_filters_non_person_and_low_confidence(self):
        with patch("detection.detector.YOLO", fake_yolo):
            detector = PersonDetector(confidence_threshold=0.5)

        self.assertEqual(
            detector.detect_people(frame="frame"),
            [Detection(xyxy=(10, 20, 30, 40), confidence=0.9, class_id=0)],
        )


if __name__ == "__main__":
    unittest.main()

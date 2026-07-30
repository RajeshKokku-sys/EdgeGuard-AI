from config.settings import Settings

from detection.detector import PersonDetector

from face.face_detector import FaceDetector
from face.face_matcher import FaceMatcher

from database.db_manager import DatabaseManager


class PersonTracker:
    """
    Camera Frame
          |
          ▼
      YOLO Detection
          |
          ▼
      ByteTrack
          |
          ▼
    Face Recognition

    Returns tracked people.
    """

    def __init__(self):
        self.detector = PersonDetector()
        self.database = DatabaseManager()
        self.face_detector = FaceDetector()
        self.face_matcher = FaceMatcher(self.database)

    def track(self, frame):
        print("=" * 60)
        print("Frame type :", type(frame))
        print("Frame shape:", frame.shape)
        print("Frame dtype:", frame.dtype)
        print("Model id   :", id(self.detector.model))

        results = self.detector.model.track(
            frame,
            persist=True,
            tracker=Settings.TRACKER_CONFIG,
            conf=Settings.DETECTION_THRESHOLD,
            verbose=True,
        )

        tracked_people = []

        if len(results) == 0:
            return results, tracked_people

        boxes = results[0].boxes

        if boxes is None:
            return results, tracked_people

        if boxes.id is None:
            return results, tracked_people

        ids = boxes.id.int().cpu().tolist()

        height, width, _ = frame.shape

        for box, track_id in zip(boxes, ids):
            cls = int(box.cls[0])

            if cls != 0:
                continue

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Boundary protection
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(width, x2)
            y2 = min(height, y2)

            person_crop = frame[y1:y2, x1:x2]

            identity = {
                "authorized": False,
                "name": "Unknown",
                "employee_id": None,
                "department": None,
                "designation": None,
                "score": 0.0,
            }

            if person_crop.size != 0:
                face = self.face_detector.get_largest_face(person_crop)

                if face is not None:
                    identity = self.face_matcher.identify(face.embedding)

            tracked_people.append({
                "track_id": track_id,
                "confidence": confidence,
                "bbox": (x1, y1, x2, y2),
                "identity": identity,
            })

        return results, tracked_people
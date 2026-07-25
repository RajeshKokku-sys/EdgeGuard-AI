import cv2

from camera.camera_manager import CameraManager
from config.settings import Settings
from detection.detector import PersonDetector
from tracking.tracker import PersonTracker
from utils.logger import get_logger

from events.event_manager import EventManager
from events.deduplication import EventDeduplicationManager
from alerts.alarm import AlarmManager
from database.db_manager import DatabaseManager
from evidence.evidence_manager import EvidenceManager

logger = get_logger("EdgeGuard")


def main():
    logger.info("Starting EdgeGuard AI")

    # Initialize modules
    camera = CameraManager(Settings.CAMERA_SOURCE)
    detector = PersonDetector(Settings.MODEL_PATH)
    tracker = PersonTracker(detector)

    event_manager = EventManager()
    dedup = EventDeduplicationManager(cooldown_seconds=10)
    alarm = AlarmManager()
    db = DatabaseManager()
    evidence = EvidenceManager()

    if not camera.is_opened():
        logger.error("Failed to open camera")
        return

    logger.info("Camera opened successfully")

    while True:
        success, frame = camera.read()

        if not success:
            break

        # ByteTrack tracking
        results = tracker.track(frame)

        annotated_frame = results[0].plot()

        boxes = results[0].boxes

        if boxes.id is not None:
            for box, track_id in zip(boxes, boxes.id.int().cpu().tolist()):
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                # Class 0 = person
                if class_id == 0:
                    logger.info(
                        f"Person ID {track_id} detected ({confidence:.2f})"
                    )

                    # Deduplication check
                    if dedup.should_create_event(track_id):
                        logger.info(
                            f"Creating new event for Person ID {track_id}"
                        )

                        event = event_manager.create_event(
                            camera_name="Main Entrance",
                            confidence=confidence,
                            track_id=track_id,
                            event_type="PERSON_DETECTED"
                        )

                        db.insert_event(event)
                        alarm.trigger(event)

                        image_path = evidence.save_snapshot(frame, event)

                        logger.info(f"Evidence saved: {image_path}")
                    else:
                        logger.info(
                            f"Duplicate event ignored for Person ID {track_id}"
                        )

        cv2.imshow("EdgeGuard AI", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    db.close()
    cv2.destroyAllWindows()

    logger.info("EdgeGuard AI stopped")


if __name__ == "__main__":
    main()
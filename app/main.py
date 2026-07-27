import cv2

from camera.camera_manager import CameraManager
from config.settings import Settings
from detection.detector import PersonDetector
from tracking.tracker import PersonTracker
from zones.zone_manager import ZoneManager

from utils.logger import get_logger

from events.event_manager import EventManager
from events.deduplication import EventDeduplicationManager

from alerts.alarm import AlarmManager
from database.db_manager import DatabaseManager
from evidence.evidence_manager import EvidenceManager


logger = get_logger("EdgeGuard")


def main():

    logger.info("Starting EdgeGuard AI")

    # ----------------------------------------
    # Initialize Modules
    # ----------------------------------------

    camera = CameraManager(Settings.CAMERA_SOURCE)

    detector = PersonDetector(Settings.MODEL_PATH)

    tracker = PersonTracker(detector)

    zone_manager = ZoneManager()

    event_manager = EventManager()

    dedup = EventDeduplicationManager(
        cooldown_seconds=10
    )

    alarm = AlarmManager()

    db = DatabaseManager()

    evidence = EvidenceManager()

    # ----------------------------------------
    # Camera Check
    # ----------------------------------------

    if not camera.is_opened():

        logger.error("Failed to open camera")

        return

    logger.info("Camera opened successfully")

    # ----------------------------------------
    # Main Loop
    # ----------------------------------------

    while True:

        success, frame = camera.read()

        if not success:
            break

        # ----------------------------------------
        # Run ByteTrack
        # ----------------------------------------

        results = tracker.track(frame)

        annotated_frame = results[0].plot()

        # ----------------------------------------
        # Draw Restricted Zones
        # ----------------------------------------

        annotated_frame = zone_manager.draw_zones(
            annotated_frame
        )

        boxes = results[0].boxes

        # ----------------------------------------
        # Process Detections
        # ----------------------------------------

        if boxes.id is not None:

            track_ids = boxes.id.int().cpu().tolist()

            for box, track_id in zip(boxes, track_ids):

                class_id = int(box.cls[0])

                confidence = float(box.conf[0])

                # Only detect persons
                if class_id != 0:
                    continue

                # Bounding Box Coordinates
                x1, y1, x2, y2 = box.xyxy[0]

                # Bottom-center of person
                center_x = int((x1 + x2) / 2)

                bottom_y = int(y2)

                # ----------------------------------------
                # Restricted Zone Check
                # ----------------------------------------

                inside, zone_name = zone_manager.check_intrusion(
                    center_x,
                    bottom_y
                )

                # Draw tracking point

                color = (0, 255, 0)

                if inside:
                    color = (0, 0, 255)

                cv2.circle(
                    annotated_frame,
                    (center_x, bottom_y),
                    5,
                    color,
                    -1
                )

                # Show Track ID

                cv2.putText(
                    annotated_frame,
                    f"ID:{track_id}",
                    (center_x + 5, bottom_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2
                )

                # ----------------------------------------
                # Only create event if inside zone
                # ----------------------------------------

                if inside:

                    logger.info(
                        f"Person {track_id} entered {zone_name}"
                    )

                    if dedup.should_create_event(track_id):

                        logger.info(
                            f"Creating intrusion event "
                            f"for Track ID {track_id}"
                        )

                        event = event_manager.create_event(

                            camera_name="Main Entrance",

                            confidence=confidence,

                            track_id=track_id,

                            event_type="ZONE_INTRUSION",

                            zone_name=zone_name

                        )

                        # Save Event

                        db.insert_event(event)

                        # Trigger Alarm

                        alarm.trigger(event)

                        # Save Evidence

                        image_path = evidence.save_snapshot(
                            frame,
                            event
                        )

                        logger.info(
                            f"Evidence saved: {image_path}"
                        )

                    else:

                        logger.info(
                            f"Duplicate intrusion ignored "
                            f"for Track ID {track_id}"
                        )

        # ----------------------------------------
        # Display
        # ----------------------------------------

        cv2.imshow(
            "EdgeGuard AI",
            annotated_frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    # ----------------------------------------
    # Cleanup
    # ----------------------------------------

    camera.release()

    db.close()

    cv2.destroyAllWindows()

    logger.info("EdgeGuard AI stopped")


if __name__ == "__main__":
    main()
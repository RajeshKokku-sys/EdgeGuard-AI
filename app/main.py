import cv2

from camera.camera_manager import CameraManager
from config.settings import Settings
from detection.detector import PersonDetector
from utils.logger import get_logger

from events.event_manager import EventManager
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

    event_manager = EventManager()
    alarm = AlarmManager()
    db = DatabaseManager()
    evidence = EvidenceManager()

    # ----------------------------------------
    # Check Camera
    # ----------------------------------------

    if not camera.is_opened():
        logger.error("Failed to open camera.")
        return

    logger.info("Camera opened successfully.")

    # ----------------------------------------
    # Main Loop
    # ----------------------------------------

    while True:

        success, frame = camera.read()

        if not success:
            logger.error("Failed to read frame.")
            break

        # ----------------------------------------
        # Run YOLO Detection
        # ----------------------------------------

        results = detector.detect(frame)

        annotated_frame = results[0].plot()

        # ----------------------------------------
        # Check Detections
        # ----------------------------------------

        for result in results:

            boxes = result.boxes

            for box in boxes:

                class_id = int(box.cls[0])

                confidence = float(box.conf[0])

                # YOLO Class 0 = Person
                if class_id == 0:

                    logger.info(
                        f"Person detected with confidence "
                        f"{confidence:.2f}"
                    )

                    # ----------------------------------------
                    # Create Event
                    # ----------------------------------------

                    event = event_manager.create_event(
                        camera_name="Main Entrance",
                        confidence=confidence,
                        event_type="PERSON_DETECTED"
                    )

                    # ----------------------------------------
                    # Save Event to Database
                    # ----------------------------------------

                    db.insert_event(event)

                    logger.info("Event stored in database.")

                    # ----------------------------------------
                    # Trigger Alarm
                    # ----------------------------------------

                    alarm.trigger(event)

                    # ----------------------------------------
                    # Save Evidence
                    # ----------------------------------------

                    image_path = evidence.save_snapshot(
                        frame,
                        event
                    )

                    logger.info(
                        f"Evidence saved: {image_path}"
                    )

        # ----------------------------------------
        # Display Frame
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

    logger.info("EdgeGuard AI stopped.")


if __name__ == "__main__":
    main()
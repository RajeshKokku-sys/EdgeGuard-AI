import cv2

from camera.camera_manager import CameraManager
from config.settings import Settings
from detection.detector import PersonDetector
from utils.logger import get_logger

logger = get_logger("EdgeGuard")


def main():
    logger.info("Starting EdgeGuard AI")

    camera = CameraManager(Settings.CAMERA_SOURCE)
    detector = PersonDetector(Settings.MODEL_PATH)

    if not camera.is_opened():
        logger.error("Camera failed")
        return

    while True:
        success, frame = camera.read()

        if not success:
            break

        results = detector.detect(frame)
        annotated_frame = results[0].plot()

        cv2.imshow("EdgeGuard AI", annotated_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
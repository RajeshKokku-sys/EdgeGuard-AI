import cv2

from camera.camera_manager import CameraManager
from tracking.tracker import PersonTracker


camera = CameraManager(0)

tracker = PersonTracker()

while True:

    ok, frame = camera.read()

    if not ok:
        break

    results, tracked_people = tracker.track(frame)

    annotated = results[0].plot()

    for person in tracked_people:

        print(
            f"Track {person['track_id']} "
            f"{person['identity']['name']} "
            f"{person['identity']['score']:.2f}"
        )

    cv2.imshow(
        "Tracker Test",
        annotated
    )

    if cv2.waitKey(1) == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()
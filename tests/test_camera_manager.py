import unittest
from unittest.mock import patch

from camera.camera_manager import CameraConfig, MultiCameraManager


class FakeCamera:
    def __init__(self, source):
        self.source = source
        self.released = False

    def is_opened(self):
        return self.source != "closed"

    def read(self):
        if self.source == "closed":
            return False, None
        return True, f"frame:{self.source}"

    def release(self):
        self.released = True


class MultiCameraManagerTest(unittest.TestCase):
    def test_reads_only_successful_frames(self):
        with patch("camera.camera_manager.CameraManager", FakeCamera):
            manager = MultiCameraManager(
                [
                    CameraConfig("main", "Main Entrance", 0),
                    CameraConfig("locker", "Locker Room", "closed"),
                ]
            )

        self.assertEqual(manager.opened_cameras(), ["main"])
        self.assertEqual(manager.read_frames(), {"main": "frame:0"})

        manager.release_all()
        self.assertTrue(all(camera.released for camera in manager.cameras.values()))


if __name__ == "__main__":
    unittest.main()

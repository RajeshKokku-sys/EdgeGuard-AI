from camera.camera_registry import CameraRegistry


registry = CameraRegistry(
    "camera/cameras.json"
)


for camera in registry.get_active_cameras():

    print(
        camera.name,
        camera.source
    )
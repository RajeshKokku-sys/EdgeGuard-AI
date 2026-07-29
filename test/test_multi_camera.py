from camera.camera_registry import CameraRegistry
from camera.multi_camera_manager import MultiCameraManager



registry = CameraRegistry(

    "camera/cameras.json"

)



manager = MultiCameraManager(

    registry.get_active_cameras()

)



manager.start()



while True:


    frames = manager.get_frames()



    for name,frame in frames.items():


        if frame is not None:

            print(
                "Received frame from",
                name
            )



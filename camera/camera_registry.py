import json

from camera.camera_config import CameraConfig



class CameraRegistry:


    def __init__(
        self,
        config_file
    ):

        self.config_file = config_file

        self.cameras = []

        self.load()



    def load(self):

        with open(
            self.config_file,
            "r"
        ) as file:


            data=json.load(file)



        for camera in data["cameras"]:


            config = CameraConfig(

                id=camera["id"],

                name=camera["name"],

                source=camera["source"],

                location=camera["location"],

                enabled=camera["enabled"]

            )


            self.cameras.append(config)



    def get_active_cameras(self):


        return [

            cam

            for cam in self.cameras

            if cam.enabled

        ]
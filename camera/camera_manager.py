import cv2


class CameraManager:


    def __init__(self, source):

        self.source = source

        self.camera = cv2.VideoCapture(
            source
        )


    def read(self):

        return self.camera.read()



    def is_opened(self):

        return self.camera.isOpened()



    def release(self):

        self.camera.release()
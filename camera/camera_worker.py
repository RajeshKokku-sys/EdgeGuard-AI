import cv2
import threading
import time


class CameraWorker(threading.Thread):

    def __init__(self, camera_config):

        super().__init__()

        self.camera = camera_config

        self.cap = None

        self.frame = None

        self.running = False

        self.connected = False


        # Lock for thread safety
        self.lock = threading.Lock()



    def run(self):

        print(
            f"Starting camera: {self.camera.name}"
        )


        self.cap = cv2.VideoCapture(
            self.camera.source
        )


        if not self.cap.isOpened():

            print(
                f"Failed to open {self.camera.name}"
            )

            self.connected = False

            return



        self.connected = True

        self.running = True


        print(
            f"{self.camera.name} connected"
        )



        while self.running:


            success, frame = self.cap.read()


            if success:


                with self.lock:

                    self.frame = frame.copy()



            else:

                print(
                    f"Frame read failed: {self.camera.name}"
                )


                self.connected = False


                break



            time.sleep(0.01)



        self.cap.release()


        print(
            f"{self.camera.name} stopped"
        )



    def get_frame(self):

        with self.lock:

            if self.frame is not None:

                return self.frame.copy()


            return None



    def is_connected(self):

        return self.connected



    def stop(self):

        self.running = False
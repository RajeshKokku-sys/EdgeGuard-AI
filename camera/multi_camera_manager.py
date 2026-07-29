from camera.camera_worker import CameraWorker



class MultiCameraManager:


    def __init__(self, cameras):

        self.workers = []


        for camera in cameras:

            worker = CameraWorker(
                camera
            )

            self.workers.append(
                worker
            )



    def start(self):

        for worker in self.workers:

            worker.start()



    def get_frames(self):

        frames = {}


        for worker in self.workers:


            frames[
                worker.camera.name
            ] = worker.get_frame()



        return frames



    def get_status(self):

        status = {}


        for worker in self.workers:


            status[
                worker.camera.name
            ] = worker.is_connected()



        return status



    def stop(self):

        for worker in self.workers:

            worker.stop()
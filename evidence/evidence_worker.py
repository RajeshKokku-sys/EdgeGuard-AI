import threading

from evidence.evidence_manager import EvidenceManager



class EvidenceWorker(threading.Thread):


    def __init__(

        self,

        evidence_queue,

        database

    ):


        super().__init__()


        self.queue = evidence_queue

        self.db = database


        self.manager = EvidenceManager()


        self.running = True



    def run(self):

        print(
            "Evidence Worker Started"
        )


        while self.running:


            task = self.queue.get_task()


            try:


                print(

                    "Processing evidence for event",

                    task.event_id

                )


                image_path = (

                    self.manager.save_snapshot(

                        task.frame,

                        task.event,

                        task.event_id

                    )

                )


                video_path = (

                    self.manager.save_video(

                        task.frames,

                        task.event,

                        task.event_id

                    )

                )


                self.db.insert_evidence(

                    task.event_id,

                    image_path,

                    video_path

                )


                print(

                    "Evidence saved"

                )


            except Exception as e:


                print(

                    "Evidence error:",

                    e

                )


            finally:


                self.queue.task_completed()



    def stop(self):

        self.running = False
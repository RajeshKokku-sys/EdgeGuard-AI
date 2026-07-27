import cv2


from camera.camera_manager import CameraManager

from config.settings import Settings

from detection.detector import PersonDetector

from tracking.tracker import PersonTracker

from zones.zone_manager import ZoneManager


from events.event_manager import EventManager

from events.deduplication import EventDeduplicationManager


from alerts.alarm import AlarmManager


from database.db_manager import DatabaseManager


from evidence.evidence_manager import EvidenceManager

from evidence.video_recorder import VideoRecorder


from utils.frame_buffer import FrameBuffer

from utils.logger import get_logger



logger = get_logger("EdgeGuard")



def main():


    logger.info(
        "Starting EdgeGuard AI"
    )


    # -----------------------------
    # Initialize Modules
    # -----------------------------


    camera = CameraManager(
        Settings.CAMERA_SOURCE
    )


    detector = PersonDetector(
        Settings.MODEL_PATH
    )


    tracker = PersonTracker(
        detector
    )


    zone_manager = ZoneManager()


    event_manager = EventManager()


    dedup = EventDeduplicationManager(
        cooldown_seconds=10
    )


    alarm = AlarmManager()


    db = DatabaseManager()


    evidence = EvidenceManager()


    video_recorder = VideoRecorder()


    frame_buffer = FrameBuffer(
        size=200
    )



    if not camera.is_opened():

        logger.error(
            "Camera failed"
        )

        return



    while True:


        success,frame = camera.read()


        if not success:
            break



        # Store frame history

        frame_buffer.add(frame)



        # ByteTrack

        results = tracker.track(
            frame
        )


        annotated_frame = results[0].plot()



        annotated_frame = zone_manager.draw_zones(
            annotated_frame
        )



        boxes = results[0].boxes



        if boxes.id is not None:


            track_ids = (
                boxes.id
                .int()
                .cpu()
                .tolist()
            )



            for box,track_id in zip(
                boxes,
                track_ids
            ):


                class_id = int(
                    box.cls[0]
                )


                confidence = float(
                    box.conf[0]
                )


                if class_id != 0:
                    continue



                x1,y1,x2,y2 = (
                    box.xyxy[0]
                )


                center_x = int(
                    (x1+x2)/2
                )


                bottom_y = int(
                    y2
                )



                inside,zone_name = (
                    zone_manager.check_intrusion(

                        center_x,

                        bottom_y

                    )
                )



                if inside:


                    if dedup.should_create_event(
                        track_id
                    ):


                        event = (
                            event_manager.create_event(

                                camera_name=
                                "Main Entrance",

                                confidence=
                                confidence,

                                track_id=
                                track_id,

                                event_type=
                                "ZONE_INTRUSION",

                                zone_name=
                                zone_name

                            )
                        )



                        # Save event

                        event_id = (
                            db.insert_event(
                                event
                            )
                        )



                        # Alarm

                        alarm.trigger(
                            event
                        )



                        # Snapshot

                        image_path = (
                            evidence.save_snapshot(

                                frame,

                                event_id

                            )
                        )



                        # Video

                        frames = (
                            frame_buffer.get_frames()
                        )


                        video_path = (

                            video_recorder.save_video(

                                frames,

                                f"evidence/videos/event_{event_id}.mp4"

                            )

                        )



                        # Map evidence

                        db.insert_evidence(

                            event_id,

                            image_path,

                            video_path

                        )



        cv2.imshow(

            "EdgeGuard AI",

            annotated_frame

        )



        if cv2.waitKey(1)&0xff == ord("q"):

            break



    camera.release()

    db.close()

    cv2.destroyAllWindows()
    
    logger.info("EdgeGuard AI stopped")


if __name__=="__main__":

    main()
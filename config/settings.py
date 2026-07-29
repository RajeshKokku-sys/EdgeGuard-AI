import os


class Settings:
    """
    Central configuration for EdgeGuard AI
    """


    # =====================================
    # Application Information
    # =====================================

    PROJECT_NAME = "EdgeGuard AI"

    VERSION = "0.9"

    ENVIRONMENT = "development"



    # =====================================
    # Camera Configuration
    # =====================================

    # USB Camera
    # 0 = Laptop webcam

    CAMERA_SOURCE = 0


    # Example RTSP camera

    # CAMERA_SOURCE = (
    #     "rtsp://username:password@camera-ip:554/stream"
    # )


    CAMERA_NAME = "Main Entrance"



    # =====================================
    # YOLO Detection Configuration
    # =====================================

    MODEL_PATH = (
        "models/yolov8n.pt"
    )


    # Person detection confidence

    DETECTION_THRESHOLD = 0.60



    # =====================================
    # ByteTrack Configuration
    # =====================================

    TRACKER_CONFIG = (
        "bytetrack.yaml"
    )


    TRACK_BUFFER = 30



    # =====================================
    # Face Recognition Configuration
    # =====================================

    FACE_MODEL_NAME = (
        "buffalo_l"
    )


    # InsightFace detection size

    FACE_DETECTION_SIZE = (
        640,
        640
    )


    # Cosine similarity threshold

    # Higher value = stricter matching

    FACE_MATCH_THRESHOLD = 0.60



    # =====================================
    # Employee Database
    # =====================================

    DATABASE_PATH = (
        "database/edgeguard.db"
    )



    # =====================================
    # Evidence Management
    # =====================================


    IMAGE_FOLDER = (
        "evidence/images"
    )


    VIDEO_FOLDER = (
        "evidence/videos"
    )


    # Video recording

    VIDEO_FPS = 20


    # Seconds of recording

    VIDEO_DURATION = 30



    # =====================================
    # Frame Buffer
    # =====================================

    # Number of frames stored

    # Used for pre-event recording


    FRAME_BUFFER_SIZE = 200



    # =====================================
    # Restricted Zone Configuration
    # =====================================


    ZONE_FILE = (
        "zones/zones.json"
    )



    # =====================================
    # Event Configuration
    # =====================================


    EVENT_COOLDOWN_SECONDS = 10



    # =====================================
    # Alarm Configuration
    # =====================================


    ALARM_ENABLED = True



    # =====================================
    # Notification Configuration
    # =====================================


    TELEGRAM_ENABLED = False


    TELEGRAM_TOKEN = os.getenv(
        "TELEGRAM_TOKEN"
    )


    TELEGRAM_CHAT_ID = os.getenv(
        "TELEGRAM_CHAT_ID"
    )



    # =====================================
    # Logging Configuration
    # =====================================


    LOG_LEVEL = (
        "INFO"
    )


    LOG_FILE = (
        "logs/edgeguard.log"
    )
    
    # =====================================
    # Telegram Configuration
    # =====================================
    
    TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
    
    TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

    # =====================================
    # Helper Method
    # =====================================


    @staticmethod
    def create_directories():

        """
        Creates required folders
        during application startup
        """

        folders = [

            "models",

            "database",

            "evidence/images",

            "evidence/videos",

            "logs"

        ]


        for folder in folders:

            os.makedirs(
                folder,
                exist_ok=True
            )
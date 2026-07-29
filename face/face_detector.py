from insightface.app import FaceAnalysis

from config.settings import Settings


class FaceDetector:
    """
    Detects faces and generates embeddings using InsightFace.
    """

    def __init__(self):

        self.app = FaceAnalysis(
            name=Settings.FACE_MODEL_NAME
        )

        self.app.prepare(
            ctx_id=0,
            det_size=Settings.FACE_DETECTION_SIZE
        )

    def detect_faces(self, image):
        """
        Returns all detected faces.
        """

        return self.app.get(image)

    def get_largest_face(self, image):
        """
        Returns the largest detected face.
        """

        faces = self.detect_faces(image)

        if len(faces) == 0:
            return None

        largest = max(
            faces,
            key=lambda f: (
                (f.bbox[2] - f.bbox[0]) *
                (f.bbox[3] - f.bbox[1])
            )
        )

        return largest
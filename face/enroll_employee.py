import cv2

from face.face_detector import FaceDetector
from face.employee_manager import EmployeeManager


def enroll_employee(

    image_path,

    employee_id,

    name,

    department,

    designation

):

    detector = FaceDetector()

    manager = EmployeeManager()

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(
            f"Unable to read image: {image_path}"
        )

    face = detector.get_largest_face(image)

    if face is None:
        raise ValueError(
            "No face detected in the image."
        )

    manager.enroll(

        employee_id,

        name,

        department,

        designation,

        face.embedding

    )

    print(
        f"{name} enrolled successfully."
    )


if __name__ == "__main__":

    enroll_employee(

        image_path="employees/Rajesh.jpg",

        employee_id="EMP001",

        name="Rajesh",

        department="Security",

        designation="Supervisor"

    )
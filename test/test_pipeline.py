import cv2

from ai_pipeline.pipeline import AIPipeline


pipeline = AIPipeline()


cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()


    if not ret:
        break


    result = pipeline.process(
        frame
    )


    cv2.imshow(
        "AI Pipeline Test",
        result["frame"]
    )


    print(
        result["detections"]
    )


    if cv2.waitKey(1) == ord("q"):
        break


cap.release()

cv2.destroyAllWindows()
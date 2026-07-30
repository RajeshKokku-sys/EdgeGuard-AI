from ultralytics import YOLO
import cv2

model = YOLO("models/yolov8n.pt")

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if ret:
    results = model.track(
        frame,
        persist=False
    )
    print("Tracking OK")

cap.release()
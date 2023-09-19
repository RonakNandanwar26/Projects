from ultralytics import YOLO
import cv2

model = YOLO('object_detection/YOLO_weights/yolov8l.pt') # It will download yolo model weights -> yolov8n = yolo version 8 nano, also can use yolov8l and yolov8m
results = model('object_detection/images/img3.jpeg', show=True)  # passing image to YOLO model for object dsetection
cv2.waitKey(0)   # to stop the result screen untill user inputs anything else result comes and go in a fraction of second , you won't be able to see.



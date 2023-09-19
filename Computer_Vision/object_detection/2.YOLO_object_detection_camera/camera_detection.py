from ultralytics import YOLO
import cv2
import cvzone

model = YOLO('object_detection/YOLO_weights/yolov8m.pt')

cap = cv2.VideoCapture(0) # in case only 1 camera use 0 -> else as per number of cameras.
cap.set(3,1280)  # width of screen
cap.set(4,720)   # height of screen

while True:
    success, image = cap.read()
    results = model(image,stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1,y1,x2,y2 = box.xyxy[0] 
            print(x1,y1,x2,y2)  # x1,y1,x2,y2 are in tensor
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            print(x1,y1,x2,y2)
            cv2.rectangle(image,(x1,y1),(x2,y2),(255,0,255),3)    # img, rectangle_dimensions, color , thickness

    cv2.imshow("Image",image)
    cv2.waitKey(1) # 0 if image , 1 for video
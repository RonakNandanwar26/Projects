from ultralytics import YOLO
import cv2
import cvzone

model = YOLO('YOLO_weights/yolov8l.pt')

# cap = cv2.VideoCapture(0) # in case only 1 camera use 0 -> else as per number of cameras.
cap = cv2.VideoCapture('videos/Bike riding.mp4') # for video

# cap.set(3,1280)  # width of screen , don't set it for video
# cap.set(4,720)   # height of screen , don't set it for video 

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag" "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana" "apple", "sandwich", "orange", "broccoli", "carrot" "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush" ] 

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

            # using opencv
            # cv2.rectangle(image,(x1,y1),(x2,y2),(255,0,255),3)    # img, rectangle_dimensions, color , thickness 

            # using cvzone
            w, h = x2-x1, y2-y1
            
            conf = round(float(box.conf[0]),4)
            print(conf)
            cls = int(box.cls[0])
            
            cvzone.cornerRect(image,(x1,y1,w,h)) # for fancy rectangle with different color corner.

            
            # cvzone.putTextRect(image,f"{classNames[cls]} : {conf}",(x1,y1))

            # getting max values as if object is passing out of window we can still see class and confidence, in above case it will be not possible
            cvzone.putTextRect(image,f"{classNames[cls]} : {conf}",(max(20,x1),max(35,y1)),scale=2,thickness=2) # scale is for size of text and thickness for thickness of text   

    cv2.imshow("Image",image)
    cv2.waitKey(1) # 0 if image , 1 for video
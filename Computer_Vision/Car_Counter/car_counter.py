from ultralytics import YOLO
import cv2
import cvzone
from sort import *

model = YOLO('YOLO_weights/yolov8n.pt')

# cap = cv2.VideoCapture(0) # in case only 1 camera use 0 -> else as per number of cameras.
cap = cv2.VideoCapture('/Users/apple/Desktop/Me/Projects/Computer_Vision/videos/cars.mp4') # for video

classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag" "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana" "apple", "sandwich", "orange", "broccoli", "carrot" "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush" ] 

## Tracker
tracker = Sort(max_age=20,min_hits=3,iou_threshold=0.3) # max_age -> detection in atlease t max_age frames, min_hits -> min number of object detect, iou -> intersection over union threshold. 

## if you want to detect car in specific region then create mask other then that region using canva and make bitwise and of image and mask
## need to make sure the mask and video is of same resolution.
cars_ids = []
total_count = 0
# to draw a line on video and count car only after this line
limits = [575,725,400,100]
while True:
    success, image = cap.read()
    # imgRegion = cv2.bitwise_and(image,mask) # read mask and use it here in case of specific region detection and pass imgRegion in model
    results = model(image,stream=True)

    
    # for tracking counts
    detection = np.empty((0,5))

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

            if classNames[cls] == 'car':            
                cvzone.cornerRect(image,(x1,y1,w,h)) # for fancy rectangle with different color corner.
                # cvzone.putTextRect(image,f"{classNames[cls]} : {conf}",(x1,y1))
    
                # getting max values as if object is passing out of window we can still see class and confidence, in above case it will be not possible
                cvzone.putTextRect(image,f"{classNames[cls]} : {conf}",(max(20,x1),max(35,y1)),scale=2,thickness=2) # scale is for size of text and thickness for thickness of text   

                # for tracking detection
                currentArray = np.array([x1,y1,x2,y2,conf]) 
                detection = np.vstack((detection,currentArray))               

    resultTracker = tracker.update(detection)
    cv2.line(image,(limits[0],limits[1]),(limits[2],limits[3]),(0,0,255),3)
    for result in resultTracker:
        x1,y1,x2,y2,id = result
        x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2-x1, y2-y1

        cx,cy = x1+w//2,y1+h//2
        print("cxcy",cx,cy)
        cv2.circle(image,(cx,cy),3,(255,0,255),cv2.FILLED)

        # limits = [575,725,400,100]
        # if (limits[0] < cx < limits[2]) and (limits[1] - 700 < cy < limits[1] + 700):
        if cars_ids.count(id) == 0:
            cars_ids.append(id)
            cv2.line(image,(limits[0],limits[1]),(limits[2],limits[3]),(0,255,0),3)
                 
        # cvzone.cornerRect(image,(x1,y1,w,h))
    
    cvzone.putTextRect(image,f"Cars : {len(cars_ids)}",(50,50),scale=2,thickness=2,colorR=(255,0,255)) # scale is for size of text and thickness for thickness of text   


    cv2.imshow("Image",image)
    cv2.waitKey(1) # 0 if image , 1 for video
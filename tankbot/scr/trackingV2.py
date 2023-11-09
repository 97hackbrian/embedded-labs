import cv2
import sys
from time import sleep
sys.path.append('/root/Desktop/embedded-labs/tankbot')
from libs.tracker import *
from libs.tiva import *
tiva1 = InitSerial(baud=9600)
motors = Motors(serial_instance=tiva1)
Leds = LedControl(serial_instance=tiva1)
Leds.init_system(cam=0)  # Repair cam=1

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture(0)

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
clahe=cv2.createCLAHE(clipLimit=30, tileGridSize=(57,57))
while True:
    ret, frame = cap.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    frame=frame[:,:,0]
    frame = clahe.apply(frame)
    #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=cv2.GaussianBlur(frame,(23,23),0)
    frame = frame[300:,: ]
    height, width = frame.shape

    # Extract Region of interest
    roi = frame[380:,: ]

    # 1. Object Detection
    mask = object_detector.apply(roi)
   #_, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
    mask = cv2.adaptiveThreshold(mask, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 40)
    mask = cv2.Canny(mask,10,1)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area <1000 and area>100:
            #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            if(x>400):
                print("derecha")
                motors.move(70,-70)
                
            elif(x<230):
                motors.move(-80,80)
                print("izquierda")
            else:
                motors.stop()
                print("centro")
            print("x= ",x)

            #detections.append([x, y, w, h])
        

    # 2. Object Tracking
    #boxes_ids = tracker.update(detections)
    
    '''for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)'''

    #cv2.imshow("roi", roi)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        motors.stop()
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import sys
from time import sleep
import numpy as np
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

# Object detection from stable camera
while True:
    ret, frame = cap.read()
    frame = frame[300:,: ]
    if not ret:
        break

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for the colors you want to detect
    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([0, 0, 0])
    lower_green = np.array([0, 0, 0])
    upper_green = np.array([0, 0, 0])
    lower_red1 = np.array([150, 50, 150])
    upper_red1 = np.array([255, 255, 255])
    lower_red2 = np.array([0, 0, 0])###
    upper_red2 = np.array([0, 0, 0])

    # Create masks for the colors
    mask_blue = cv2.inRange(frame_hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(frame_hsv, lower_green, upper_green)
    mask_red1 = cv2.inRange(frame_hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(frame_hsv, lower_red2, upper_red2)

    # Combine the red masks to handle the wrap-around in the hue space
    mask_red = mask_red1 + mask_red2

    # Combine all masks
    mask = mask_blue + mask_green + mask_red

    mask=cv2.GaussianBlur(mask,(11,11),0)

    # Find contours in the combined mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    if len(contours)>=1 and len(contours)<=6:
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            
            
            if area > 15000:
                print("cnt ",len(cnt))
                if len(cnt)>=1000:
                    Leds.write(1,1,0,0)
                    sleep(0.01)
                    Leds.write(0,0,1,1)
                    sleep(0.01)
                    motors.stop()

                else:
                    x, y, w, h = cv2.boundingRect(cnt)
                    center_x = x + w // 2

                    if center_x > 420:
                        print("derecha")
                        motors.move(70, -70)
                    elif center_x < 210:
                        print("izquierda")
                        motors.move(-84, 84)
                    else:
                        print("centro")
                        motors.stop()
    else:
        print("AQUI!!!!!!!!!!")
        motors.move(-75, 75)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        motors.stop()
        break

cap.release()
cv2.destroyAllWindows()

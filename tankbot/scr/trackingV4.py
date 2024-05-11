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

pid=[0,0,0]
k=[0.000001,0.005,0]
errorAnt=0
setpoint=640/2
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

    # Find contours in the combined mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            center_x = x + w // 2
            error=center_x-setpoint
            pid[0]=k[0]*error
            pid[2]=(error-errorAnt)*k[2]

            # Interpolate PID[0] from 60 to 100
            interpolated_pid = min(80, max(50, 50 + (sum(pid) + 80) / 2.0))
            print("Interpolated PID:", interpolated_pid)

            # Control the motors with the interpolated PID value
            if center_x > 430:
                motors.move(int(interpolated_pid), -int(interpolated_pid))
            elif center_x < 220:
                motors.move(-int(interpolated_pid), int(interpolated_pid))
            else:
                motors.stop()
            errorAnt=error

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        motors.stop()
        break

cap.release()
cv2.destroyAllWindows()

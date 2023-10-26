
import numpy as np
from pixie import Camara, img, showIMG, video, videosPlays
import RPi.GPIO as GPIO
import serial
import time
import cv2

serial=serial.Serial("/dev/ttyACM0",9600,timeout=1)
serial.reset_input_buffer()
serial.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
class video():
    def __init__(self, camera) -> None:
        self.camera = camera
        self.displayed = False
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()

    def display_camera(self):
        self.displayed = True
        self.camera_visualization()
    
    def stop_display(self):
        self.displayed = False

    def count_objects(self, contours):
        return len(contours)

    def preprocess_foreground(self, foreground_mask):
        kernel = np.ones((20,20),np.uint8)
        foreground_mask = cv2.erode(foreground_mask, kernel, iterations = 1)
        foreground_mask = cv2.dilate(foreground_mask, kernel, iterations = 1)
        foreground_mask = cv2.morphologyEx(foreground_mask, cv2.MORPH_OPEN, kernel)
        return foreground_mask

    def camera_visualization(self):
        while self.displayed:
            check, frame = self.camera.read()
            if not check:
                print("Error: Unable to capture frame.")
                self.stop_display()
            key = cv2.waitKey(1)
            if key == 27:
                self.stop_display()

            foreground_mask = self.background_subtractor.apply(frame)
            _, thresh = cv2.threshold(foreground_mask, 244, 255, cv2.THRESH_BINARY)
            processed_foreground = self.preprocess_foreground(thresh)

            contours, _ = cv2.findContours(processed_foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contours, -1, (255, 255, 255), 2)  # Cambia a (0, 0, 0) para negro
            num_objects = self.count_objects(contours)
            if num_objects > 0:
                if num_objects == 1:
                    serial.write("2\n".encode())
                    print("ONE")
                else :
                    serial.write("4\n".encode())
                    print("MORE")
            else:
                print("No Move")
                serial.write("0\n".encode())

            cv2.imshow("Processed Foreground", processed_foreground)
            cv2.imshow("Video", frame)

if __name__ == "__main__":
    camera = cv2.VideoCapture(0)
    camera_object = video(camera)
    camera_object.display_camera()
    camera.release()
    cv2.destroyAllWindows()

import RPi.GPIO as GPIO
import serial
import time
import numpy as np

ser=serial.Serial("/dev/ttyACM0",9600,timeout=1)
ser.reset_input_buffer()
ser.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

while(True):
    try:
        duty=input("ingrese pwm: ")
        ser.write((duty+'\n').encode())
    except:
        print("error")


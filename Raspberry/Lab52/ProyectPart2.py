import RPi.GPIO as GPIO
import serial
import time
import numpy as np

ser=serial.Serial("/dev/ttyACM1",9600,timeout=1)
ser.reset_input_buffer()
ser.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

while(True):
    
   # arrayR = np.loadtxt('Raspberry/Lab52/time2.txt')
    #print(arrayR)
    a=input("ingrese tiempo: ")
    a=str(a+"\n")
    ser.write(a.encode())

    
    

    
import RPi.GPIO as GPIO
import serial
import time
import numpy as np
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)



GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
valor_anterior = None
while(True):
    try:
        with open('Raspberry/Lab4/time.txt', 'r') as file:
            arrayR = file.readline().strip()

        print("VALOR:", arrayR)
        GPIO.output(5,1)
        
        time.sleep(int(arrayR))  
        GPIO.output(6,1)
        time.sleep(int(arrayR))
        GPIO.output(5,0)
        
        time.sleep(int(arrayR))
        GPIO.output(6,0)
        time.sleep(int(arrayR))



    except Exception as e:
        print("Error:", str(e))

    

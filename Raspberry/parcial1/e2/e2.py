import RPi.GPIO as GPIO
import serial
import time

serial=serial.Serial("/dev/ttyACM0",9600,timeout=1)
serial.reset_input_buffer()
serial.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

boton=2
GPIO.setup(boton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
while(True):
    try:
        if(GPIO.input(boton) == GPIO.LOW):
            serial.write("reset\n".encode())
            #uart envia led on
        else:
            serial.write("none\n".encode())

        
        
            
        

    except:
        print("No connected ERROR")
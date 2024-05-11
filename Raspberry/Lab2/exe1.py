import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

led = 13 
led2 = 26
boton = 2

gpio.setup(led,gpio.OUT)
gpio.setup(led2,gpio.OUT)
gpio.setup(boton,gpio.IN, pull_up_down=gpio.PUD_UP)

flag=0

while(1):
    val = gpio.input(boton)
    if(val == 0):
        while(1):
            if(val == 1 and flag == 1):
                flag = 0
                break
            gpio.output(led,1)
            gpio.output(led2,1)
            time.sleep(2)
            gpio.output(led,0)
            gpio.output(led2,0)
            time.sleep(2)
            val = gpio.input(boton)
            if(val == 0):
                while(1):
                    val = gpio.input(boton)
                    if(val == 1):
                        flag =1
                        break
                    

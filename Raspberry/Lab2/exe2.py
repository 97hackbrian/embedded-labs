import RPi.GPIO as gpio
import continuous_threading
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
flag2=0
val =0
def bot ():
    while (1):
        if (flag == 1):
            gpio.output(led,1)
            gpio.output(led2,1)
            time.sleep(2)
            gpio.output(led,0)
            gpio.output(led2,0)
            time.sleep(2)

timer1 = continuous_threading.ContinuousThread(target=bot)
timer1.start()

while(1):
    val = gpio.input(boton)
    
    
    if(val == 0 and flag == 0):
        while(1):
            val = gpio.input(boton)
            if(val == 1):
                flag =1
                break
    val = gpio.input(boton)

    if(val == 0 and flag ==1):
        while(1):
            val = gpio.input(boton)
            if(val == 1):
                gpio.output(led,0)
                gpio.output(led2,0)
                flag =0
                break

                
    continuous_threading.shutdown(0)
                    

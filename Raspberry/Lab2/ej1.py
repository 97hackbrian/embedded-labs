import RPi.GPIO as gpio 
import time
gpio.setwarnings(False) 
gpio.setmode(gpio.BCM)
gpio.setup(24, gpio.OUT) 
gpio.setup(13, gpio.OUT)



gpio.setup(2, gpio.IN, pull_up_down=gpio.PUD_UP) 
state_led = 0

while True: 
    button = gpio.input(2) 
    print (button)
    if button == 0:
        state_led = state_led + 1 
        time.sleep(1)

    if state_led == 0:
        gpio.output(24,True) #Encendido
        gpio.output(13,False) #apagado
        time.sleep(1)
        gpio.output(24,False) 
        gpio.output(13,True) 
        time.sleep(1) 

    if state_led == 1: 
        gpio.output(24,True)
        gpio.output(13,True)

        time.sleep(2) 

        gpio.output(24,False)
        gpio.output(13,False)

        time.sleep(2) 

    if state_led == 2: 
        gpio.output(24,True)
        gpio.output(13,True)

        #time.sleep(10) 

    if state_led == 3:
        gpio.output(24,False)
        gpio.output(13,False)

        time.sleep(10) # 2 sec delay
    if state_led == 4: 
        state_led = 0 
        #time.sleep(2)
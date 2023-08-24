import RPi.GPIO as gpio 
import time
gpio.setwarnings(False) 
gpio.setup(12, gpio.OUT) 
gpio.setup(16, gpio.OUT)



gpio.setup(14, gpio.IN, pull_up_down=gpio.PUD_UP) 
state_led = 0

while True: 
    button = gpio.input(14) 
    print (button)
    if button == 0:
        state_led = state_led + 1 
        time.sleep(1)

    if state_led == 0:
        gpio.output(12,True) #Encendido
        gpio.output(16,False) #apagado
        time.sleep(1)
        gpio.output(12,False) 
        gpio.output(16,True) 
        time.sleep(1) 

    if state_led == 1: 
        gpio.output(12,True)
        gpio.output(16,True)

        time.sleep(2) 

        gpio.output(12,False)
        gpio.output(16,False)

        time.sleep(2) 

    if state_led == 2: 
        gpio.output(12,True)
        gpio.output(16,True)

        #time.sleep(10) 

    if state_led == 3:
        gpio.output(12,False)
        gpio.output(16,False)

        time.sleep(10) # 2 sec delay
    if state_led == 4: 
        state_led = 0 
        #time.sleep(2)
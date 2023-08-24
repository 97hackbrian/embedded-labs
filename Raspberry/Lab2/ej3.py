import RPi.GPIO as gpio 
import time
import random

gpio.setwarnings(False) 
gpio.setup(12, gpio.OUT) 
gpio.setup(16, gpio.OUT)



gpio.setup(14, gpio.IN, pull_up_down=gpio.PUD_UP) 
state_led = 0

while True: 
    rand = random.randit(1,30)
    temperature = rand
    if temperature >=12 and temperature <=20:
        GPIO.output(14, False)
        GPIO.output(15, False)
    elif temperature <12:
        GPIO.output(15, True)
    elif temperature >20:
        GPIO.output(14, True)
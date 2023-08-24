import RPi.GPIO as gpio 
import time
import random
gpio.setmode(gpio.BCM)
gpio.setwarnings(False) 
gpio.setup(24, gpio.OUT) 
gpio.setup(13, gpio.OUT)



gpio.setup(14, gpio.IN, pull_up_down=gpio.PUD_UP) 
state_led = 0

while True: 
    rand = random.randint(1,30)
    print("temp: ",rand)
    time.sleep(1)
    temperature = rand
    if temperature >=12 and temperature <=20:
        gpio.output(24, False)
        gpio.output(13, False)
    elif temperature <12:
        gpio.output(24, True)
    elif temperature >20:
        gpio.output(13, True)
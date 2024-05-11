from gpiozero import Servo
from time import sleep

servo = Servo(27)

try:
    while True:
        servo.value=-1
        sleep(5)
        servo.value=0
        sleep(5)
except KeyboardInterrupt:
    print("Program stopped")
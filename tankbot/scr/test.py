from time import sleep
import sys
sys.path.append('tankbot/')
from libs.tiva import *


if __name__ == "__main__":
    tiva1=InitSerial(baud=9600)
    motors=Motors(serial_instance=tiva1)
    Leds=LedControl(serial_instance=tiva1)
    Leds.init_system(cam=0)##reparar cam=1
    
    motors.stop()
    motors.move(50,50)
    Leds.write(0,1,0,1)
    sleep(3)
    motors.move(60,60)
    Leds.write(1,0,1,0)
    sleep(3)
    motors.stop()
    Leds.write(0,0,1,1)
    sleep(5)
    motors.move(-60,60)
    Leds.write(1,1,0,0)
    sleep(3)
    motors.stop()
    Leds.write(0,0,0,0)

import RPi.GPIO as GPIO
from time import sleep

in1 = 14
in2 = 15
en = 18
DutyCycle = 100

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.HIGH)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(0)


while(1):
        p.ChangeDutyCycle(DutyCycle)
        print("Duty Cycle", DutyCycle)
        sleep(0.0)

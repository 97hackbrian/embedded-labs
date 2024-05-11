import RPi.GPIO as GPIO
import time
import serial
import numpy as np

serial=serial.Serial("/dev/ttyACM1",9600,timeout=1)
serial.reset_input_buffer()
serial.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

IN1=27
IN2=22
PWMA=13
IN3=5
IN4=6
PWMB=12

class MotorController():
    def __init__(self,IN1,IN2,PWMA,IN3,IN4,PWMB):
        GPIO.setup(IN1,GPIO.OUT)
        GPIO.setup(IN2,GPIO.OUT)
        GPIO.setup(PWMA,GPIO.OUT)

        GPIO.setup(IN3,GPIO.OUT)
        GPIO.setup(IN4,GPIO.OUT)
        GPIO.setup(PWMB,GPIO.OUT)
        self.IN1=IN1
        self.IN2=IN2
        self.IN3=IN3
        self.IN4=IN4

        self.pwma=GPIO.PWM(PWMA,50)
        self.pwmb=GPIO.PWM(PWMB,50)
        self.pwma.start(0)
        self.pwmb.start(0)


    def left(self, vel1):
        if(vel1>0):
            GPIO.output(self.IN1,GPIO.HIGH)
            GPIO.output(self.IN2,GPIO.LOW)
            self.pwma.ChangeDutyCycle(vel1)
        else:
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
            self.pwma.ChangeDutyCycle(vel1*-1)


    def right(self,vel2):
        if(vel2>0):
            GPIO.output(self.IN3,GPIO.HIGH)
            GPIO.output(self.IN4,GPIO.LOW)
            self.pwmb.ChangeDutyCycle(vel2)
        else:
            GPIO.output(self.IN3,GPIO.LOW)
            GPIO.output(self.IN4,GPIO.HIGH)
            self.pwmb.ChangeDutyCycle(vel2*-1)


motors=MotorController(IN1,IN2,PWMA,IN3,IN4,PWMB)
defR=5
defL=5

motors.right(defR)
motors.left(defL)
time.sleep(3)
while(True):
    try:
        arrayR = np.loadtxt('/root/Desktop/embedded-labs/Raspberry/brayanp1/dutys.txt')
        motors.right(arrayR[0])
        motors.left(arrayR[1])
        print("left motor=",arrayR[0],"and right motor=",arrayR[1])
        if(arrayR[0]==0 or arrayR[1]==0):
            serial.write("buzzer\n".encode())
        else:
            serial.write("none\n".encode())
        time.sleep(1)
    except:
        print("error")
        
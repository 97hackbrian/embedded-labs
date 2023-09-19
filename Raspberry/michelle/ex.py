import RPi.GPIO as GPIO
import serial
import time
import numpy as np

ser=serial.Serial("/dev/ttyACM0",9600,timeout=1)
ser.reset_input_buffer()
ser.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

IN1=27
IN2=22
PWMA=13
IN3=5
IN4=6
PWMB=12
booton=2

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
    def move(self,vel1,vel2):
        if(vel1>0):
            GPIO.output(self.IN1,GPIO.HIGH)
            GPIO.output(self.IN2,GPIO.LOW)
            self.pwma.ChangeDutyCycle(vel1)
        else:
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
            self.pwma.ChangeDutyCycle(vel1*-1)

        if(vel2>0):
            GPIO.output(self.IN3,GPIO.HIGH)
            GPIO.output(self.IN4,GPIO.LOW)
            self.pwmb.ChangeDutyCycle(vel2)
        else:
            GPIO.output(self.IN3,GPIO.LOW)
            GPIO.output(self.IN4,GPIO.HIGH)
            self.pwmb.ChangeDutyCycle(vel2*-1)

    def stop(self):
        GPIO.output(self.IN1,GPIO.LOW)
        GPIO.output(self.IN2,GPIO.LOW)
        self.pwma.ChangeDutyCycle(0)
        GPIO.output(self.IN3,GPIO.LOW)
        GPIO.output(self.IN4,GPIO.LOW)
        self.pwmb.ChangeDutyCycle(0)

motors=MotorController(IN1,IN2,PWMA,IN3,IN4,PWMB)

GPIO.setup(booton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
while(True):
    try:
        arrayR = np.loadtxt('Raspberry/Lab5/duty.txt')
        value=ser.readline().decode('utf-8').rstrip()
        print("VALOR: ",value)
        if(value=="motor1"):
            motors.move(arrayR[0],0)
        elif(value=="motor2"):
            motors.move(0,arrayR[1])
        if(value=="notpressed"):
            motors.move(0,0)
        if(GPIO.input(booton) == GPIO.LOW):
            ser.write("buzzer\n".encode())
            #ser.reset_output_buffer()
            #time.sleep(1)
        else:
            ser.write("none\n".encode())
    except:
        print("error")


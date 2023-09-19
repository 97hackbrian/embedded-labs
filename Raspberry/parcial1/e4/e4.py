import RPi.GPIO as GPIO
import serial
import time

serial=serial.Serial("/dev/ttyACM0",9600,timeout=1)
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

default=19

class component_pwm():
    def __init__(self):
        IN1=27
        IN2=22
        PWMA=13
        IN3=5
        IN4=6
        PWMB=12
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

        
    
    def component_state(self,duty,state):
        #pass
        if(state==1):
            if(duty>0):
                GPIO.output(self.IN1,GPIO.HIGH)
                GPIO.output(self.IN2,GPIO.LOW)
                self.pwma.ChangeDutyCycle(duty)
            else:
                GPIO.output(self.IN1,GPIO.LOW)
                GPIO.output(self.IN2,GPIO.HIGH)
                self.pwma.ChangeDutyCycle(duty*-1)
            
        else:
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.LOW)
            self.pwma.ChangeDutyCycle(0)
    


class motor_pwm(component_pwm):
    def __init__(self):
        #pass
        super().__init__()
        

motor=motor_pwm()
dutydefault=0
anstate=0
statedefault=0

motor.component_state(0,1)
while(True):
    try:
        value=serial.readline().decode('utf-8').rstrip()
        
        if(value=="pressed1"):
            
            dutydefault=dutydefault+5
            print("duty+",dutydefault)

        if(value=="pressed0"):
            statedefault = 1 - statedefault  # Alternar entre 0 y 1
            print("motorON" if statedefault == 1 else "motorOFF")
       
        
        
            
        
       

        print("duty=",dutydefault, "  state",statedefault)
        motor.component_state(int(dutydefault),statedefault)
        

    except:
        print("No connected ERROR")
    

   
import RPi.GPIO as GPIO
import continuous_threading
import time

buzzers=[26,13]
bootons=[2,3]
class buzzer:
    def __init__(self,buzz,buttons):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.buzzers=buzz
        self.botones=buttons
        self.flag=0
        for pin in buzz:
            GPIO.setup(pin,GPIO.OUT)
        for pin in buzz:
            GPIO.output(pin,0)

        for pin in buttons:
            GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
        self.th = continuous_threading.ContinuousThread(target=self.sonar)
        self.th.start()
    def sonar (self):
        while True:

            if(self.flag==1):
                for pin in self.buzzers:
                    GPIO.output(pin,1)
                time.sleep(1/1000000)
                for pin in self.buzzers:
                    GPIO.output(pin,0)
                time.sleep(1/1000000)
            else:
                for pin in self.buzzers:
                    GPIO.output(pin,0)
    def refresh(self):
        if(GPIO.input( self.botones[0] ) == GPIO.LOW):
            self.flag=1
            
        else:
            self.flag=0
        continuous_threading.shutdown(0)

Pulbuzzer=buzzer(buzzers,bootons)
while True:
    Pulbuzzer.refresh()
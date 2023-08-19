import RPi.GPIO as GPIO
import time


'''led1=5
led2=6
led3=13
led4=26'''

led=[23,24,13,26]

#bott1=17
#bott2=27
bootons=[2,3]

class counterTime:
	def __init__(self,leds,buttons):
		self.count=0
		self.countT=1
		self.pinleds=leds
		self.botones=buttons
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		for pin in leds:
			GPIO.setup(pin,GPIO.OUT)

		for pin in buttons:
			GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

	def addT (self):
		if(self.countT>=1):
			self.countT=self.countT+1
		else:
			self.countT=1
		#print(self.count)

	def change (self):
		if(self.count>(len(self.pinleds)-2)):
			self.count=0
		else:
			self.count=self.count+1
		#print(self.count)
		
	
	def refresh(self):
		if(GPIO.input( self.botones[0] ) == GPIO.LOW):
			self.addT()
			time.sleep(0.7)
		elif(GPIO.input( self.botones[1] ) == GPIO.LOW):
			self.change()
			self.countT=1
			time.sleep(0.7)
		GPIO.output(self.pinleds[self.count],1)
		time.sleep(self.countT)
		GPIO.output(self.pinleds[self.count],0)
		time.sleep(1)



counterTimes=counterTime(led,bootons)
while True:
	counterTimes.refresh()



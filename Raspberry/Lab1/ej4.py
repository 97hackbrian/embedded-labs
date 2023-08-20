import RPi.GPIO as GPIO
import continuous_threading
import time

led=[23,24,13,26]

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
		for pin in leds:
			GPIO.output(pin,0)

		for pin in buttons:
			GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

		self.th = continuous_threading.ContinuousThread(target=self.Actions)
		self.th.start()
    	

	def addT (self):
		if(self.countT>=1):
			self.countT=self.countT+1
		else:
			self.countT=1


	def change (self):
		if(self.count>(len(self.pinleds)-2)):
			self.count=0
		else:
			self.count=self.count+1

	def Actions(self):
		while True:
			GPIO.output(self.pinleds[self.count],1)
			time.sleep(self.countT)
			GPIO.output(self.pinleds[self.count],0)
			time.sleep(1)
		
	def refresh(self):
		if(GPIO.input( self.botones[0] ) == GPIO.LOW):
			while True:
				if(GPIO.input( self.botones[0] ) == GPIO.HIGH):
					self.addT()
					time.sleep(0.3)
					print("Time+1= ",self.countT)
					break

		elif(GPIO.input( self.botones[1] ) == GPIO.LOW):
			'''for pin in self.pinleds:
						GPIO.output(pin,0)'''
			while True:
				if(GPIO.input( self.botones[1] ) == GPIO.HIGH):
					self.countT=1
					GPIO.output(self.pinleds[self.count],0)
					self.change()
					time.sleep(0.2)
					print("Led [",self.count,"]")
					break
		
		continuous_threading.shutdown(0)
		



counterTimes=counterTime(led,bootons)
while True:
	counterTimes.refresh()



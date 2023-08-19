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

class counter:
	def __init__(self,leds,buttons):
		self.count=0
		self.pinleds=leds
		self.botones=buttons
		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		for pin in leds:
			GPIO.setup(pin,GPIO.OUT)

		for pin in buttons:
			GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

	def add (self):
		if(self.count<=14):
			self.count=self.count+1
		else:
			self.count=0
		#print(self.count)

	def less (self):
		if(self.count==0):
			self.count=0
		else:
			self.count=self.count-1
		#print(self.count)
		
	
	def refresh(self):
		if(GPIO.input( self.botones[0] ) == GPIO.LOW):
			self.add()
			time.sleep(0.7)
		elif(GPIO.input( self.botones[1] ) == GPIO.LOW):
			self.less()
			time.sleep(0.7)
		outs=format(self.count,"b")
		outs=outs.zfill(4)
		print(outs)
		flag=0
		for pin in self.pinleds:
			GPIO.output(pin,int(outs[flag]))
			flag=flag+1



counter1=counter(led,bootons)
while True:
	counter1.refresh()



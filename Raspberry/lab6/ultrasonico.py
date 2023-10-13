
import RPi.GPIO as GPIO
import time
import serial
ser=serial.Serial("/dev/ttyACM0",9600,timeout=1)
ser.reset_input_buffer()
ser.reset_output_buffer()

TRIG = 18 
ECHO = 24 
GPIO.setmode(GPIO.BCM)            
GPIO.setup(TRIG, GPIO.OUT) 
GPIO.setup(ECHO, GPIO.IN)   



try:
    
    while True:

        
        GPIO.output(TRIG, GPIO.LOW)
        time.sleep(0.5)

        
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)

        
        
        while True:
            pulso_inicio = time.time()
            if GPIO.input(ECHO) == GPIO.HIGH:
                break

        
        
        while True:
            pulso_fin = time.time()
            if GPIO.input(ECHO) == GPIO.LOW:
                break

        
        duracion = pulso_fin - pulso_inicio

        
        distancia = (34300 * duracion) / 2

        
        print( "Distancia: %.2f cm" % distancia)

        if(distancia>=10):
            ser.write("1\n".encode())
        elif(distancia>=8 and distancia<10):
            ser.write("2\n".encode())
        elif(distancia>=6 and distancia<8):
            ser.write("3\n".encode())
        elif(distancia>=4 and distancia<6):
            ser.write("4\n".encode())
        else:
            ser.write("5\n".encode())

finally:
    
    GPIO.cleanup()
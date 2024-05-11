import RPi.GPIO as GPIO
import serial
import time
import numpy as np

ser=serial.Serial("/dev/ttyACM0",9600,timeout=1)
ser.reset_input_buffer()
ser.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
valor_anterior = None
while(True):
    try:
        with open('/root/Desktop/embedded-labs/Raspberry/parcial1/e3/duty.txt', 'r') as file:
            arrayR = file.readline().strip()

        print("VALOR:", arrayR)

        # Verifica si el valor ha cambiado desde la última vez que se envió
        if arrayR != valor_anterior:
            if arrayR == "stop":
                ser.write("0\n".encode())
            else:
                ser.write(str(arrayR + "\n").encode())
            valor_anterior = arrayR  # Actualiza el valor anterior

    except Exception as e:
        print("Error:", str(e))

    time.sleep(1)  # Espera un segundo antes de verificar nuevamente

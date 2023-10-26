from pixie import Camara, img, showIMG, video, videosPlays
import RPi.GPIO as GPIO
import serial
import time
import cv2

serial=serial.Serial("/dev/ttyACM0",9600,timeout=1)
serial.reset_input_buffer()
serial.reset_output_buffer()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
motion=0
cap = cv2.VideoCapture(0) 
ret, framex = cap.read()
frame1=img(framex,"RGB")
frame1.resize_img(50,50,0)
gray1 = cv2.cvtColor(frame1.imagen, cv2.COLOR_BGR2GRAY)

while True:
    # Captura un nuevo fotograma
    ret, frame3 = cap.read()
    frame2=img(frame3,"RGB")
    frame2.resize_img(50,50,0)
    # Convierte el fotograma a escala de grises
    gray2 = cv2.cvtColor(frame2.imagen, cv2.COLOR_BGR2GRAY)

    # Calcula la diferencia entre los dos fotogramas
    frame_delta = cv2.absdiff(gray1, gray2)

    # Aplica un umbral a la diferencia para resaltar el movimiento
    _, thresh = cv2.threshold(frame_delta, 30, 255, cv2.THRESH_BINARY)

    # Encuentra y dibuja los contornos del área con movimiento
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Puedes ajustar este valor según tus necesidades
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2.imagen, (x, y), (x + w, y + h), (0, 255, 0), 2)
            motion=1
            #time.sleep(2)
            print("motion detect")
        else:
            motion=0
            print("static")
        if(motion==1):
            
            serial.write("buzzer\n".encode())
            time.sleep(4)
            serial.write("none\n".encode())
            
        else:
            serial.write("none\n".encode())
            

    # Muestra el fotograma con el movimiento detectado
    cv2.imshow('Motion Detection', frame2.imagen)
    
    # Actualiza el fotograma anterior
    gray1 = gray2

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    

# Libera la cámara y cierra las ventanas
cap.release()
cv2.destroyAllWindows()

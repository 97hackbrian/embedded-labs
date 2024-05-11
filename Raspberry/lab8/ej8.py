from pixie import Camara, img, showIMG, video, videosPlays

import serial
import time
import cv2

serial=serial.Serial("/dev/ttyACM0",9600,timeout=1)
serial.reset_input_buffer()
serial.reset_output_buffer()


motion=0
cap = cv2.VideoCapture(0) 
ret, framex = cap.read()
frame1=img(framex,"BGR")
frame1.resize_img(50,50,0)
gray1 = cv2.cvtColor(frame1.imagen, cv2.COLOR_BGR2GRAY)

while True:
    ret, frame3 = cap.read()
    frame2=img(frame3,"BGR")
    frame2.resize_img(50,50,0)
    gray2 = cv2.cvtColor(frame2.imagen, cv2.COLOR_BGR2GRAY)

    # Calcula la diferencia entre los dos fotogramas
    frame_delta = cv2.absdiff(gray1, gray2)

    _, thresh = cv2.threshold(frame_delta, 55, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 80:  
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2.imagen, (x, y), (x + w, y + h), (0, 255, 0), 2)
            motion=1
            print("motion detect")
        else:
            motion=0
            print("static")
        if(motion==1):
            
            serial.write("buzzer\n".encode())
            time.sleep(0.3)
            serial.write("none\n".encode())
            
        else:
            serial.write("none\n".encode())
            

    cv2.imshow('Motion Detection', frame2.imagen)
    
    gray1 = gray2

    # Sale del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Libera la cámara y cierra las ventanas
cap.release()
cv2.destroyAllWindows()

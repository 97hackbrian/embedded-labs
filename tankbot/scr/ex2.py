import cv2
import sys
from time import sleep
import numpy as np
sys.path.append('/root/Desktop/embedded-labs/tankbot')
from libs.tracker import *
from libs.tiva import *

def detect(contour):
    """
    Función que, dado un contorno, retorna la forma geométrica más cercana con base al número de lados del perímetro del
    mismo.
    :param contour: Contorno del que inferiremos una figura geométrica.
    :return: Texto correspondiente a la figura geométrica identificada (TRIANGULO, CUADRADO, RECTANGULO, PENTAGONO o CIRCULO)
    """
    # Hallamos el perímetro (cerrado) del contorno.
    perimeter = cv2.arcLength(contour, True)

    # Aproximamos un polígono al contorno, con base a su perímetro.
    approximate = cv2.approxPolyDP(contour, .04 * perimeter, True)
    x, y, w, h = cv2.boundingRect(approximate)
    aspect_ratio = w / float(h)

  
    
    
    if ((len(approximate) ==4)and (aspect_ratio==1 )):
        shape = 'cuadrado'
    elif ((len(approximate) ==3)and (aspect_ratio>=1 and aspect_ratio<=1.5  )):
        shape = 'triangulo'
    elif ((len(approximate) ==7)and (aspect_ratio>=0.8 and aspect_ratio<1)):
        shape = 'circulo'
    

        
    # Por defecto, asumiremos que cualquier polígono con 6 o más lados es un círculo.
    
    else:
        shape = ' '

    return shape,len(approximate),aspect_ratio

def classify_color(hsv_color):
    hue = hsv_color[0]

    if (0 <= hue <= 10) or (160 <= hue <= 180):
        return "morado"  # Círculo
    elif 10 <= hue <= 20:
        return "naranja"  # Triángulo
    else:
        return "negro"  # Cuadrado

tiva1 = InitSerial(baud=9600)
motors = Motors(serial_instance=tiva1)
Leds = LedControl(serial_instance=tiva1)
Leds.init_system(cam=0)

tracker = EuclideanDistTracker()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = frame[300:, :]

    if not ret:
        break

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([0, 0, 0])
    upper_blue = np.array([0, 0, 0])
    lower_green = np.array([0, 0, 0])
    upper_green = np.array([0, 0, 0])
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 150, 255])
    lower_red2 = np.array([160, 50, 50])
    upper_red2 = np.array([180, 150, 255])

    mask_blue = cv2.inRange(frame_hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(frame_hsv, lower_green, upper_green)
    mask_red1 = cv2.inRange(frame_hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(frame_hsv, lower_red2, upper_red2)

    mask_red = mask_red1 + mask_red2

    mask = mask_blue + mask_green + mask_red

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            shape, _, _ = detect(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            center_x = x + w // 2
            color = classify_color(frame_hsv[y + h // 2, x + w // 2])
            
            if shape == 'cuadrado' and color == "negro":
                print("Cuadrado - Color: " + color)
            elif shape == 'triangulo' and color == "naranja":
                print("Triángulo - Color: " + color)
            elif shape == 'circulo' and color=morado:
                print("Círculo - Color: " + color)

            else:
                print("centro")
                motors.stop()

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27:
        motors.stop()
        break

cap.release()
cv2.destroyAllWindows()
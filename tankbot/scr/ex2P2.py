import cv2
import sys
from time import sleep
import numpy as np
sys.path.append('/root/Desktop/embedded-labs/tankbot')
from libs.tracker import *
from libs.tiva import *
ra=0
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

  
    
    
    if ((len(approximate) ==4)and (aspect_ratio>=0.5 and aspect_ratio<=4 )):
        shape = 'cuadrado'
    

        
    # Por defecto, asumiremos que cualquier polígono con 6 o más lados es un círculo.
    
    else:
        shape = ' '

    return shape,len(approximate),aspect_ratio

def classify_color(hsv_color):
    hue = hsv_color[0]

    if (100 <= hue <= 255):# or (200 <= hue <= 180):
        return "morado"  # Círculo = 274,70,62
    elif 0 <= hue <= 99:
        return "naranja"  # Triángulo = 24,79,92
    else:
        return "negro"  # Cuadrado = 0,0,25

tiva1 = InitSerial(baud=9600)
motors = Motors(serial_instance=tiva1)
Leds = LedControl(serial_instance=tiva1)
Leds.init_system(cam=0)

tracker = EuclideanDistTracker()

cap = cv2.VideoCapture(0)
con=0
while True:
    ret, frame = cap.read()
    #frame = frame[100:, :]
    frame=cv2.GaussianBlur(frame,(15,15),0)
    if not ret:
        break

    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    lower_morado = np.array([200, 90, 100])
    upper_morado = np.array([255, 150, 180])
    lower_naranja = np.array([1, 48, 100])
    upper_naranja = np.array([200, 125, 200])
    lower_negro = np.array([90, 90, 90])
    upper_negro = np.array([120, 120, 120])
    #lower_red2 = np.array([160, 50, 50])
    #upper_red2 = np.array([180, 150, 255])

    mask_morado = cv2.inRange(frame_hsv, lower_morado, upper_morado)
    mask_naranja = cv2.inRange(frame_hsv, lower_naranja, upper_naranja)
    mask_negro = cv2.inRange(frame_hsv, lower_negro, upper_negro)
    _,mask_negro2 =   cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
    #mask_red2 = cv2.inRange(frame_hsv, lower_red2, upper_red2)

    #mask_red = mask_red1 + mask_red2

    mask = mask_negro2
    contoursCanny=cv2.Canny(mask,0,100)
    #contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours2, _ = cv2.findContours(contoursCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    def FocalLength(measured_distance, real_width, width_in_rf_image): 
        focal_length = (width_in_rf_image* measured_distance)/ real_width 
        return focal_length 
    for cnt in contours2:
        area = cv2.contourArea(cnt)
        
        if area > 10000:
            
    
            print("area: ",area)
            shape2,lin,ra=detect(cnt)
            if shape2=="cuadrado":
                shape,count,ratio = shape2,lin,ra
                con=con+1
                cv2.drawContours(frame, [cnt], -1, (255, 255, 0), 2)  # Dibuja el contorno en la imagen RGB
                
                cv2.putText(frame, str(shape)+str(con), tuple(cnt[0][0]+40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3)
                cv2.putText(frame, str(count), tuple(cnt[0][0]+90), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3)
                cv2.putText(frame, str(ratio), tuple(cnt[0][0]+130), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3)
                x, y, w, h = cv2.boundingRect(cnt)
                center_x = x + w // 2
                #color = classify_color(frame_hsv[y + h // 2, x + w // 2])
                #dir=FocalLength(ra,10,10)
                if area<=50000:
                    
                    motors.move(60,60)
                    print("avanzar!")
                else:
                    motors.stop()
                    print("stop!")
                    
                #print(" ratio ",ra)

            else:
                    motors.stop()
                    print("stop!")
        
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", contoursCanny)

    key = cv2.waitKey(30)
    if key == 27:
        motors.stop()
        break

cap.release()
cv2.destroyAllWindows()

import cv2


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
        shape = 'Cuadrado'
    elif ((len(approximate) ==3)and (aspect_ratio>=1 and aspect_ratio<=1.5  )):
        shape = 'Triangulo'
    elif ((len(approximate) ==5)and (aspect_ratio>=1 and aspect_ratio<=1.5  )):
        shape = 'Pentagono'
    elif ((len(approximate) ==7)and (aspect_ratio>=0.8 and aspect_ratio<1)):
        shape = 'circulo'
    elif ((len(approximate) ==6)and (aspect_ratio>=1 and aspect_ratio<=1.5  )):
        shape = 'hexagono'
    elif ((len(approximate) ==4)and (aspect_ratio>=2)):
        shape = 'Rectangulo'

        
    # Por defecto, asumiremos que cualquier polígono con 6 o más lados es un círculo.
    
    else:
        shape = ' '

    return shape,len(approximate),aspect_ratio

imgcolor=cv2.imread("/root/Desktop/embedded-labs/Raspberry/Lab9/recursos_lab_9/figuras.png",1)
img=cv2.cvtColor(imgcolor,cv2.COLOR_BGR2GRAY)
contoursCanny=cv2.Canny(img,0,100)
contours, _ = cv2.findContours(contoursCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#shape,lados,ratio=detect(img)
image_rgb = imgcolor
con=0
for contour in contours:
    
    shape,count,ratio = detect(contour)  # Llama a la función detect para clasificar la forma
    
    con=con+1
    cv2.drawContours(image_rgb, [contour], -1, (255, 255, 0), 2)  # Dibuja el contorno en la imagen RGB
    
    cv2.putText(image_rgb, str(shape)+str(con), tuple(contour[0][0]+40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3)
    cv2.putText(image_rgb, str(count), tuple(contour[0][0]+90), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3)
    cv2.putText(image_rgb, str(ratio), tuple(contour[0][0]+130), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 0, 0), 3)
cv2.imshow("figuras",image_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()

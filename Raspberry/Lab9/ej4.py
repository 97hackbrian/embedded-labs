import cv2
import numpy as np

# Cargar la imagen
color = cv2.imread('/home/hackbrian/Documentos/gitProyects/embedded-labs/Raspberry/Lab9/recursos_lab_9/monedas_2.jpg')
img = cv2.imread('/home/hackbrian/Documentos/gitProyects/embedded-labs/Raspberry/Lab9/recursos_lab_9/monedas_2.jpg', cv2.IMREAD_GRAYSCALE)
img=cv2.resize(img,(600,400))
color=cv2.resize(color,(600,400))
# Aplicar la adaptación del umbral gaussiano
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11, 1)

# Aplicar el desenfoque gaussiano
#img = cv2.GaussianBlur(img, (5, 5), 0)

# Aplicar Canny para encontrar bordes
#contoursCanny = cv2.Canny(img, 0, 200)

# Detectar círculos utilizando HoughCircles
circles = cv2.HoughCircles(
    img, 
    cv2.HOUGH_GRADIENT, dp=1, minDist=115,
    param1=100, param2=15, minRadius=65, maxRadius=70
)

con=0
# Si se detectan círculos, dibujarlos
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        con=con+1
        # Dibujar el círculo exterior
        cv2.circle(color, (i[0], i[1]), i[2], (0, 255, 0), 2)
        # Dibujar el centro del círculo
        cv2.circle(color, (i[0], i[1]), 2, (0, 0, 255), 3)
        cv2.putText(color, str(con), (i[0], i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 110, 100), 3)

# Mostrar la imagen con círculos detectados
cv2.imshow('Circulos Detectados', color)
cv2.waitKey(0)
cv2.destroyAllWindows()

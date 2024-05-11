import cv2

captura = cv2.VideoCapture(0)
contador_imagenes = 1

while True:
    ret, frame = captura.read()
    cv2.imshow('Webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        ruta_imagen = f'/home/hackbrian/gitProyects/embedded-labs/Raspberry/lab7/Capturas/image{contador_imagenes}.jpg'
        cv2.imwrite(ruta_imagen, frame)
        print(f"Imagen guardada en {ruta_imagen}")
        contador_imagenes += 1

    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

captura.release()
cv2.destroyAllWindows()

imagen_grayscale = cv2.imread(ruta_imagen, cv2.IMREAD_GRAYSCALE)
filas, columnas = imagen_grayscale.shape
centro_filas, centro_columnas = filas // 2, columnas // 2

cuadrante_superior_izquierdo = imagen_grayscale[:centro_filas, :centro_columnas]
cuadrante_superior_derecho = imagen_grayscale[:centro_filas, centro_columnas:]
cuadrante_inferior_izquierdo = imagen_grayscale[centro_filas:, :centro_columnas]
cuadrante_inferior_derecho = imagen_grayscale[centro_filas:, centro_columnas:]

cv2.imshow('Cuadrante Superior Izquierdo', cuadrante_superior_izquierdo)
cv2.imshow('Cuadrante Superior Derecho', cuadrante_superior_derecho)
cv2.imshow('Cuadrante Inferior Izquierdo', cuadrante_inferior_izquierdo)
cv2.imshow('Cuadrante Inferior Derecho', cuadrante_inferior_derecho)

cv2.waitKey(0)
cv2.destroyAllWindows()
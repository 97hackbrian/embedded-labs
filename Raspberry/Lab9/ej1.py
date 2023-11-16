import cv2

# Cargar el video
cap = cv2.VideoCapture('Raspberry/Lab9/recursos_lab_9/bouncing.mp4')

# Seleccionar el algoritmo de sustracción de fondo
#subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
#subtractor = cv2.createBackgroundSubtractorMOG2()
subtractor = cv2.createBackgroundSubtractorKNN() #mejor
#subtractor = cv2.bgsegm.createBackgroundSubtractorGMG()



while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Aplicar el algoritmo de sustracción de fondo al frame actual
    fg_mask = subtractor.apply(frame)

    # Visualizar el resultado
    cv2.imshow('Foreground Mask', fg_mask)

    if cv2.waitKey(30) & 0xFF == 27:  # Presionar 'Esc' para salir
        break

cap.release()
cv2.destroyAllWindows()

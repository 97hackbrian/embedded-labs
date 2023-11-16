from pixie import img, showIMG, video, videosPlays
import cv2

videCon = []

if __name__ == "__main__":
    video1 = video()
    video1.load("Raspberry/Lab9/recursos_lab_9/bouncing.mp4")

    videOriginal = video1.retorno()
    
    for frame in videOriginal:
        # Aplicar el algoritmo Canny
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 80, 240)

        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar contornos en el frame original
        cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

        videCon.append(frame)

    videosPlays(video1, [videCon])

import cv2


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()


grayscale_mode = False

while True:

    ret, frame = cap.read()


    if not ret:
        print("Error: Could not read frame.")
        break


    if grayscale_mode:

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('Webcam (Grayscale)', gray_frame)
    else:

        cv2.imshow('Webcam (RGB)', frame)


    key = cv2.waitKey(1)


    if key == ord('g'):
        grayscale_mode = not grayscale_mode
    elif key == ord('r'):
        grayscale_mode =  grayscale_mode
    elif key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
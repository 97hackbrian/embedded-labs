import cv2
import numpy as np

# Open the webcam
cap = cv2.VideoCapture(0)  # Use 0 for default webcam
desired_width = 640
desired_height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)

desired_fps = 30
cap.set(cv2.CAP_PROP_FPS, desired_fps)
# Create a background subtractor
subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    frame=cv2.GaussianBlur(frame,(19,19),0)
    fg_mask = subtractor.apply(frame)

    # Threshold the foreground mask to obtain binary image
    _, thresh = cv2.threshold(fg_mask, 128, 255, cv2.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Iterate through the contours
    for contour in contours:
        # Calculate the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)

        # Check if the object is passing through the middle of the frame
        if x < frame.shape[1] // 2 < x + w and y < frame.shape[0] // 2 < y + h:
            cv2.putText(frame, "Object Detected", (frame.shape[1] - 200, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw the bounding box around the object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Object Detection', frame)

    # Break the loop if 'Esc' key is pressed
    if cv2.waitKey(30) & 0xFF == 27:
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()

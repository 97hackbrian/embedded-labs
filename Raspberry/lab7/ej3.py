import cv2
from pynput import keyboard

def rotate_image(image, degrees):
    height, width = image.shape[:2]
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, degrees, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
    return rotated_image

image = cv2.imread('conejo2.jpg')  # Replace 'your_image.jpg' with the path to your image

current_rotation = 0

def on_key_press(key):
    global current_rotation
    try:
        current_rotation += 90
        current_rotation %= 360
        rotated_image = rotate_image(image, current_rotation)
        cv2.imshow("Rotated Image", rotated_image)
        cv2.waitKey(0)
    except AttributeError:
        pass

def on_key_release(key):
    pass

with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
    listener.join()

cv2.destroyAllWindows()
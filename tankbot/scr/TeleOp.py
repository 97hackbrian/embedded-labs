from time import sleep
import sys
sys.path.append('/root/Desktop/embedded-labs/tankbot')
from libs.tiva import *
from pynput.keyboard import Key, Listener

# Define the initial velocities
left_velocity = 0
right_velocity = 0

# Function to update motor velocities and LED control
def update_motors_and_leds():
    motors.move(left_velocity, right_velocity)
    Leds.write(0, 1, 0, 1)  # You can change the LED pattern here

# Function to handle key presses
def on_key_press(key):
    global left_velocity, right_velocity
    if key == Key.up:
        left_velocity = 70
        right_velocity = 70
    elif key == Key.down:
        left_velocity = -60
        right_velocity = -60
    elif key == Key.left:
        left_velocity = -80
        right_velocity = 80
    elif key == Key.right:
        left_velocity = 70
        right_velocity = -70
    update_motors_and_leds()

# Function to handle key releases
def on_key_release(key):
    sleep(0.7)
    global left_velocity, right_velocity
    if key in (Key.up, Key.down, Key.left, Key.right):
        left_velocity = 0
        right_velocity = 0
        motors.stop()
        Leds.write(0, 0, 0, 0)

if __name__ == "__main__":
    tiva1 = InitSerial(baud=9600)
    motors = Motors(serial_instance=tiva1)
    Leds = LedControl(serial_instance=tiva1)
    Leds.init_system(cam=0)  # Repair cam=1

    update_motors_and_leds()

    # Create listener for key events
    with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

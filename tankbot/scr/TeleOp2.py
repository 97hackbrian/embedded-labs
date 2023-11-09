from time import sleep
import sys
sys.path.append('/root/Desktop/embedded-labs/tankbot')
from libs.tiva import *
from pynput.keyboard import Key, Listener

# Define the initial velocities
left_velocity = 0
right_velocity = 0

# Define two velocity options
velocities = {
    '1': 50,
    '2': 100
}

# Current velocity option
current_velocity = 50  # Default to 50

# Function to update motor velocities and LED control
def update_motors_and_leds():
    motors.move(left_velocity, right_velocity)
    #Leds.write(0, 1, 0, 1)  # You can change the LED pattern here

# Function to handle key presses
def on_key_press(key):
    global left_velocity, right_velocity, current_velocity
    if key == Key.up:
        left_velocity = current_velocity
        right_velocity = current_velocity
    elif key == Key.down:
        left_velocity = -current_velocity
        right_velocity = -current_velocity
    elif key == Key.left:
        left_velocity = -current_velocity
        right_velocity = current_velocity
    elif key == Key.right:
        left_velocity = current_velocity
        right_velocity = -current_velocity
    elif key == Key.esc:  # Exit the program with the Esc key
        listener.stop()
        return
    elif key == Key.space:  # Stop the motors with the Space key
        left_velocity = 0
        right_velocity = 0
        motors.stop()
        
    elif key.char in velocities:  # Check if a number key (1 or 2) is pressed
        if(key.char=="1"):
            Leds.write(1, 0, 0, 0)
        elif(key.char=="2"):
            Leds.write(0, 1, 0, 0)
        current_velocity = velocities[key.char]
        print(f"Selected velocity: {current_velocity}")
    update_motors_and_leds()

# Function to handle key releases
def on_key_release(key):
    global left_velocity, right_velocity
    if key in (Key.up, Key.down, Key.left, Key.right):
        left_velocity = 0
        right_velocity = 0
        motors.stop()
        #Leds.write(0, 0, 0, 0)

if __name__ == "__main__":
    tiva1 = InitSerial(baud=9600)
    motors = Motors(serial_instance=tiva1)
    Leds = LedControl(serial_instance=tiva1)
    Leds.init_system(cam=0)  # Repair cam=1

    update_motors_and_leds()

    # Create listener for key events
    with Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

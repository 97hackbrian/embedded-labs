from time import sleep
import sys
sys.path.append('/home/ubuntu/Desktop/embedded-labs/tankbot')
from libs.tiva import *
from pynput import keyboard

# Define the initial velocities
left_velocity = 0
right_velocity = 0
gripper_velocity = 0
mosfet_state = 0

# Variable to keep track of mos state
mos = False

# Function to update motor velocities and LED control
def update_motors_and_leds():
    motors.move(left_velocity, right_velocity)
    gripper.move(gripper_velocity)
    mosfets.activate_mosfets("x",int(mos),"x", "x", "x", "x")
    Leds.write(0, 1, 0, 1)  # You can change the LED pattern here

# Function to handle key presses
def on_key_press(key):
    global left_velocity, right_velocity, gripper_velocity, mosfet_state, mos

    if key == keyboard.Key.up:
        left_velocity = 25
        right_velocity = 25
    elif key == keyboard.Key.down:
        left_velocity = -25
        right_velocity = -25
    elif key == keyboard.Key.left:
        left_velocity = -25
        right_velocity = 25
    elif key == keyboard.Key.right:
        left_velocity = 25
        right_velocity = -25
    elif key == keyboard.Key.shift:
        gripper_velocity = 55
    elif key == keyboard.Key.ctrl:
        gripper_velocity = -40
    elif key == keyboard.KeyCode.from_char('y'):
        mos = not mos  # Toggle the mos state
    elif key == keyboard.KeyCode.from_char('Y'):
        gripper_velocity = 0  # Stop the gripper if 'Y' is pressed

    update_motors_and_leds()

# Function to handle key releases
def on_key_release(key):
    global left_velocity, right_velocity, gripper_velocity, mosfet_state
    gripper.move(0)
    if key in (keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right,
               keyboard.Key.shift, keyboard.Key.ctrl):
        left_velocity = 0
        right_velocity = 0
        gripper_velocity = 0
        motors.stop()
        Leds.write(0, 0, 0, 0)

if __name__ == "__main__":
    tiva1 = InitSerial(baud=9600)
    motors = Motors(serial_instance=tiva1)
    Leds = LedControl(serial_instance=tiva1)
    gripper = Gripper(serial_instance=tiva1)
    mosfets = Mosfets(serial_instance=tiva1)
    Leds.init_system(cam=0)  # Repair cam=1

    update_motors_and_leds()

    # Create listener for key events
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

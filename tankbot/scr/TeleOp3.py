from time import sleep
import sys
sys.path.append('/root/Desktop/embedded-labs/tankbot')
from libs.tiva import *
import pygame

# Define the initial velocities
left_velocity = 0
right_velocity = 0

# Define two velocity options
velocities = {
    '1': 100,
    '2': 125
}

# Current velocity option>
current_velocity = 30  # Default to 50

# Function to update motor velocities and LED control
def update_motors_and_leds():
    motors.move(left_velocity, right_velocity)
    # Leds.write(0, 1, 0, 1)  # You can change the LED pattern here

# Initialize pygame
pygame.init()

# Function to handle key presses
def on_key_press(key):
    global left_velocity, right_velocity, current_velocity
    if key == pygame.K_UP:
        left_velocity = current_velocity
        right_velocity = current_velocity
    elif key == pygame.K_DOWN:
        left_velocity = -current_velocity
        right_velocity = -current_velocity
    elif key == pygame.K_LEFT:
        left_velocity = -current_velocity
        right_velocity = current_velocity
    elif key == pygame.K_RIGHT:
        left_velocity = current_velocity
        right_velocity = -current_velocity
    elif key == pygame.K_ESCAPE:  # Exit the program with the Esc key
        pygame.quit()
        sys.exit()
    elif key == pygame.K_SPACE:  # Stop the motors with the Space key
        left_velocity = 0
        right_velocity = 0
        motors.stop()
    elif key.isdigit() and key in velocities:  # Check if a number key (1 or 2) is pressed
        if key == "1":
            Leds.write(1, 0, 0, 0)
        elif key == "2":
            Leds.write(0, 1, 0, 0)
        current_velocity = velocities[key]
        print(f"Selected velocity: {current_velocity}")
    update_motors_and_leds()

if __name__ == "__main__":
    tiva1 = InitSerial(baud=9600)
    motors = Motors(serial_instance=tiva1)
    Leds = LedControl(serial_instance=tiva1)
    Leds.init_system(cam=0)  # Repair cam=1

    update_motors_and_leds()

    # Main event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                on_key_press(event.key)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    left_velocity = 0
                    right_velocity = 0
                    motors.stop()
        update_motors_and_leds()
        sleep(0.01)  # Add a small delay to control the loop speed

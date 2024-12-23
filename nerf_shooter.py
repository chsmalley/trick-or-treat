from gpiozero import Motor
import time

# CONSTANTS

# GPIO PINS
TRIGGER_MOTOR_FORWARD_PIN = 17
TRIGGER_MOTOR_BACKWARD_PIN = 18
PITCH_MOTOR_FORWARD_PIN = 23
PITCH_MOTOR_BACKWARD_PIN = 24
BARREL_MOTOR_FORWARD_PIN = 7
BARREL_MOTOR_BACKWARD_PIN = 8

MAX_PITCH_PIN = 2
MIN_PITCH_PIN = 3

JAM_DOOR_PIN = 20
JAM_PIN = 21



def shoot_dart(trigger: Motor, barrel: Motor):
    

if __name__ == '__main__':
    # Create Motor objects
    trigger_motor = Motor(forward=TRIGGER_MOTOR_FORWARD_PIN,
                          backward=TRIGGER_MOTOR_BACKWARD_PIN)
    barrel_motor = Motor(forward=BARREL_MOTOR_FORWARD_PIN,
                         backward=BARREL_MOTOR_BACKWARD_PIN)
    pitch_motor = Motor(forward=PITCH_MOTOR_FORWARD_PIN,
                        backward=PITCH_MOTOR_FORWARD_PIN)

    print("Nerf shooter")
    shoot_dart()
    print("\ngoodbye")


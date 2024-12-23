from gpiozero import Motor, Button
import time

# CONSTANTS
BARREL_SPEED = 0.5
TRIGGER_SPEED = 0.5
TRIGGER_DELAY = 0.2
TRIGGER_TIME = 0.5
PITCH_SPEED = 0.5
PITCH_TIME = 0.5

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



def shoot_dart(trigger: Motor, barrel: Motor) -> None:
    barrel.forward(BARREL_SPEED)
    time.sleep(TRIGGER_DELAY)
    trigger.forward(TRIGGER_SPEED)
    time.sleep(TRIGGER_TIME)
    trigger.stop()
    barrel.stop()


# def raise_motor(pitch: Motor, max_pitch: Button) -> None:
#     while not 

if __name__ == '__main__':
    # Create Motor objects
    trigger_motor = Motor(forward=TRIGGER_MOTOR_FORWARD_PIN,
                          backward=TRIGGER_MOTOR_BACKWARD_PIN)
    barrel_motor = Motor(forward=BARREL_MOTOR_FORWARD_PIN,
                         backward=BARREL_MOTOR_BACKWARD_PIN)
    pitch_motor = Motor(forward=PITCH_MOTOR_FORWARD_PIN,
                        backward=PITCH_MOTOR_FORWARD_PIN)
    max_pitch = Button(MAX_PITCH_PIN)
    min_pitch = Button(MIN_PITCH_PIN)
    
    print("Nerf shooter")
    shoot_dart()
    print("\ngoodbye")


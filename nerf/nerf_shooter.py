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
# PITCH PINS
MAX_PITCH_PIN = 2
MIN_PITCH_PIN = 3
# SHOOTER PINS
JAM_DOOR_PIN = 20
JAM_PIN = 21


def shoot_dart(trigger: Motor,
               barrel: Motor,
               jam_button) -> None:
    barrel.forward(BARREL_SPEED)
    end_time = time.time() + TRIGGER_DELAY
    while time.time() < end_time:
        print(f"trigger state: {jam_button.is_pressed}")
        time.sleep(0.1)
    trigger.forward(TRIGGER_SPEED)
    end_time = time.time() + TRIGGER_TIME
    while time.time() < end_time:
        print(f"trigger state: {jam_button.is_pressed}")
        time.sleep(0.1)
    trigger.stop()
    barrel.stop()

def raise_motor(pitch: Motor, max_pitch: Button) -> None:
    stop_time = time.time() + PITCH_TIME
    pitch.forward()
    while not max_pitch.is_pressed and time.time() < stop_time:
        print(max_pitch.is_pressed)
        time.sleep(0.1)
    pitch.stop()

def lower_motor(pitch: Motor, min_pitch: Button) -> None:
    stop_time = time.time() + PITCH_TIME
    pitch.backward()
    while not min_pitch.is_pressed and time.time() < stop_time:
        print(min_pitch.is_pressed)
        time.sleep(0.1)
    pitch.stop()

def main():
    # Create Motor objects
    jam_button = Button(JAM_PIN)
    door_button = Button(JAM_DOOR_PIN)
    max_pitch = Button(MAX_PITCH_PIN)
    min_pitch = Button(MIN_PITCH_PIN)
    trigger_motor = Motor(forward=TRIGGER_MOTOR_FORWARD_PIN,
                          backward=TRIGGER_MOTOR_BACKWARD_PIN)
    barrel_motor = Motor(forward=BARREL_MOTOR_FORWARD_PIN,
                         backward=BARREL_MOTOR_BACKWARD_PIN)
    pitch_motor = Motor(forward=PITCH_MOTOR_FORWARD_PIN,
                        backward=PITCH_MOTOR_BACKWARD_PIN)
    
    print("Nerf shooter")
    shoot_dart(trigger_motor, barrel_motor, jam_button)
    print("raise pitch")
    raise_motor(pitch_motor, max_pitch)
    print("lower pitch")
    lower_motor(pitch_motor, min_pitch)
    print("\ngoodbye")


if __name__ == '__main__':
    main()

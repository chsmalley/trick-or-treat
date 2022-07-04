import sys
from gpiozero import Motor, Button, LED, DigitalOutputDevice
import time
import sphero_mini
import random

# CONSTANTS
TREAT_TIME = 2
BUBBLE_TIME = 2
LADDER_TIME = 10
ROLL_TIME = 5
ROLL_STEP_TIME = 0.1
BUTTON_PRESS_DELAY = 0.1
BIRD_TIME = 3
CAR_DRIVE_TIME = 3
SPHERO_SPEED = 100  # Int 0 - 255
TRICKS = (
    "BUBBLE",
    "BIRD",
    "SPHERO",
    "LADDER",
    "LIGHTS",
    "BIRD",
)
# GPIO PINS
TREAT_BUTTON_PIN = 2
BUBBLE_BUTTON_PIN = 3
TREAT_LED_PIN = 20
BUBBLE_LED_PIN = 21
TREAT_MOTOR_FORWARD_PIN = 4
TREAT_MOTOR_BACKWARD_PIN = 14
BUBBLE_MOTOR_FORWARD_PIN = 4
BUBBLE_MOTOR_BACKWARD_PIN = 14
LADDER_PIN = 26
LIGHTS_PIN = 19
BIRD_PIN = 13
CAR_FORWARD_PIN = 6
CAR_BACKWARD_PIN = 5

# Trick or Treat object to handle devices
class TrickOrTreat():
    def __init__(self, sphero_mac: str):
        self.running = False
        # Setup motors
        self.treat_motor = Motor(forward=TREAT_MOTOR_FORWARD_PIN,
                                 backward=TREAT_MOTOR_BACKWARD_PIN)
        self.bubble_motor = Motor(forward=BUBBLE_MOTOR_FORWARD_PIN,
                                  backward=BUBBLE_MOTOR_BACKWARD_PIN)
        # Setup buttons
        self.treat_button = Button(TREAT_BUTTON_PIN)
        self.bubble_button = Button(BUBBLE_BUTTON_PIN)
        # Setup LEDs
        self.treat_led = LED(TREAT_LED_PIN)
        self.bubble_led = LED(BUBBLE_LED_PIN)
        # Setup sphero ball
        self.sphero = sphero_mini.sphero_mini(sphero_mac)
        # Setup other tricks
        self.jacobs_ladder = DigitalOutputDevice(LADDER_PIN)
        self.lights = DigitalOutputDevice(LIGHTS_PIN)
        self.bird = DigitalOutputDevice(BIRD_PIN)
        self.car_forward = DigitalOutputDevice(CAR_FORWARD_PIN)
        self.car_backward = DigitalOutputDevice(CAR_BACKWARD_PIN)

    def _bubble_trick(self):
        self.bubble_motor.forward()
        self.bubble_led.on()
        time.sleep(BUBBLE_TIME)
        self.bubble_motor.stop()
        self.bubble_led.off()

    def _ladder_trick(self):
        self.jacobs_ladder.on()
        time.sleep(LADDER_TIME)
        self.jacobs_ladder.off()

    def _lights_trick(self):
        self.lights.on()
        time.sleep(LADDER_TIME)
        self.lights.off()

    def _bird_trick(self):
        # Need to mimic pressing remote control button
        self.bird.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.bird.off()
        time.sleep(BIRD_TIME)
        # Mimic button press again
        self.bird.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.bird.off()

    def _car_trick(self):
        # Need to press remote control button to drive
        self.car_forward.on()
        time.sleep(CAR_DRIVE_TIME)
        self.car_forward.off()
        time.sleep(CAR_DRIVE_TIME)
        self.car_backward.on()
        time.sleep(CAR_DRIVE_TIME)
        self.car_backward.off()

    def _sphero_trick(self):
        self.sphero.setLEDColor(red=255, green=0, blue=0)
        for i in range(ROLL_TIME // ROLL_STEP_TIME):
            self.sphero.roll(SPHERO_SPEED, 360 * i * ROLL_STEP_TIME / ROLL_TIME)
            self.sphero.wait(ROLL_STEP_TIME)
        self.sphero.roll(0, 0)
        self.sphero.wait(1)
        self.sphero.setLEDColor(red=0, green=0, blue=255)
        
    def _treat(self):
        self.treat_led.on()
        self.treat_motor.forward()
        time.sleep(TREAT_TIME)
        # self.treat_motor.backward()
        # time.sleep(TREAT_TIME)
        # self.treat_motor.forward()
        # time.sleep(TREAT_TIME)
        self.treat_motor.stop()
        self.treat_led.off()
    
    def run(self):
        self.running = True
        while self.running:
            if self.treat_button.is_pressed:
                print("treat button pressed")
                self._treat()
            elif self.bubble_button.is_pressed:
                trick = random.choice(TRICKS)
                print(f"trick button pressed. Performing trick: {trick}")
                if trick == "BUBBLE":
                    self._bubble_trick()
                elif trick == "SPHERO":
                    self._sphero_trick()
                elif trick == "LADDER":
                    self._ladder_trick()
                elif trick == "LIGHTS":
                    self._lights_trick()
                else:
                    print(f"Unknown trick: {trick}")
            else:
                # Don't run too fast
                time.sleep(0.01)

    def stop(self):
        self.running = False

if __name__ == '__main__':
    sphero_mac = sys.argv[1]
    print("Welcome trick or treaters")
    trick_or_treat = TrickOrTreat(sphero_mac)
    try:
        trick_or_treat.run()
    except KeyboardInterrupt:
        trick_or_treat.stop()
    print("goodbye")


import sys
from gpiozero import Motor, Button, LED, DigitalOutputDevice
import time
import sphero_mini
import random
import threading
import queue

# CONSTANTS
TREAT_TIME = 2
BUBBLE_TIME = 2
LADDER_TIME = 10
ROLL_TIME = 3
ROLL_STEP_TIME = 0.01
BUTTON_PRESS_DELAY = 0.1
BIRD_TIME = 3
CAR_DRIVE_TIME = 3
SPHERO_SPEED = 100  # Int 0 - 255
TRICKS = [
    "BUBBLE",
    "BIRD",
    "LADDER",
    # "SPHERO"
]
# GPIO PINS
TREAT_BUTTON_PIN = 2
BUBBLE_BUTTON_PIN = 3
TREAT_LED_PIN = 20
BUBBLE_LED_PIN = 21
TREAT_MOTOR_FORWARD_PIN = 23
TREAT_MOTOR_BACKWARD_PIN = 24
BUBBLE_MOTOR_FORWARD_PIN = 27
BUBBLE_MOTOR_BACKWARD_PIN = 17
LADDER_PIN_ON = 26
LADDER_PIN_OFF = 19
BIRD_PIN = 13
CAR_FORWARD_PIN = 6
CAR_BACKWARD_PIN = 5

# Trick or Treat object to handle devices
class TrickOrTreat():
    def __init__(self, sphero_mac: str):
        self.running = False
        self.trick_queue = queue.Queue()
        self.treat_queue = queue.Queue()
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
        if sphero_mac:
            self.sphero = sphero_mini.sphero_mini(sphero_mac)
            TRICKS.append("SPHERO")
        else:
            self.sphero = None
        # Setup other tricks
        self.jacobs_ladder_on = DigitalOutputDevice(LADDER_PIN_ON)
        self.jacobs_ladder_off = DigitalOutputDevice(LADDER_PIN_OFF)
        self.bird = DigitalOutputDevice(BIRD_PIN)
        self.car_forward = DigitalOutputDevice(CAR_FORWARD_PIN)
        self.car_backward = DigitalOutputDevice(CAR_BACKWARD_PIN)
        # Setup tricks thread
        self.trick_thread = threading.Thread(target=self._handle_tricks)
        # Setup treats thread
        self.treat_thread = threading.Thread(target=self._handle_treats)
        
    def _handle_treats(self):
        while self.running:
            treat = self.treat_queue.get()
            if treat == "CANDY":
                self._treat()
        
    def _handle_tricks(self):
        while self.running:
            trick = self.trick_queue.get()
            print(f"trick button pressed. Performing trick: {trick}")
            if trick == "BUBBLE":
                self._bubble_trick()
            elif trick == "SPHERO":
                self._sphero_trick()
            elif trick == "LADDER":
                self._ladder_trick()
            elif trick == "BIRD":
                self._bird_trick()
            else:
                print(f"Unknown trick: {trick}")
            
    def _bubble_trick(self):
        self.bubble_motor.forward()
        self.bubble_led.on()
        time.sleep(BUBBLE_TIME)
        self.bubble_motor.stop()
        self.bubble_led.off()

    def _ladder_trick(self):
        self.jacobs_ladder_on.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.jacobs_ladder_on.off()
        time.sleep(LADDER_TIME)
        self.jacobs_ladder_off.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.jacobs_ladder_off.off()

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

    def _sphero_trick2(self):
        self.sphero.setLEDColor(red=255, green=0, blue=0)
        for i in range(int(ROLL_TIME // ROLL_STEP_TIME)):
            self.sphero.roll(SPHERO_SPEED, int(360 * i * ROLL_STEP_TIME / ROLL_TIME))
            self.sphero.wait(ROLL_STEP_TIME)
        self.sphero.roll(0, 0)
        self.sphero.wait(1)
        self.sphero.setLEDColor(red=0, green=0, blue=255)

    def _sphero_trick(self):
        self.sphero.setLEDColor(red=255, green=0, blue=0)
        start_time = time.time()
        while (time.time() - start_time) < ROLL_TIME:
            self.sphero.roll(SPHERO_SPEED, random.randint(0, 360))
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
        # Start threads
        self.trick_thread.start()
        self.treat_thread.start()
        while self.running:
            if self.treat_button.is_pressed:
                print("treat button pressed")
                self.treat_queue.put("CANDY")
            elif self.bubble_button.is_pressed:
                self.trick_queue.put(random.choice(TRICKS))
            else:
                # Don't run too fast
                time.sleep(0.01)

    def stop(self):
        self.running = False
        if self.sphero is not None:
            self.sphero.disconnect()

if __name__ == '__main__':
    # EB:B6:31:82:7C:F0
    # sphero_mac = sys.argv[1]
    sphero_mac = "EB:B6:31:82:7C:F0"
    print("Welcome trick or treaters")
    trick_or_treat = TrickOrTreat(sphero_mac)
    try:
        trick_or_treat.run()
    except KeyboardInterrupt:
        trick_or_treat.stop()
    print("\ngoodbye")


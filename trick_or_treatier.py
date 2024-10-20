import sys
from gpiozero import Motor, Button, LED, DigitalOutputDevice
import time
import sphero_mini
import random
import threading
import queue
from itertools import cycle
import logging

logging.basicConfig(
    filename="trick_or_treat.log",
    format='%(asctime)s,%(levelname)s,%(message)s',
    datefmt='%Y-%m-%d,%H:%M:%S',
    level=logging.INFO
)

# CONSTANTS
TRICK_TIME = 13
TREAT_TIME = 0.2
LIGHTS_TIME = 1.0
ROLL_TIME = 3
ROLL_STEP_TIME = 0.01
BUTTON_PRESS_DELAY = 0.1
EYE_TIME = 15
BIRD_TIME = 45
SPHERO_SPEED = 100  # int: (0 - 255)
CANDY_SPEED = 0.3  # float: (0 - 1)
BLOOD_SPEED = 0.5  # float: (0 - 1)
STIR_SPEED = 0.2  # float: (0 - 1)
TRICKS = [
    "BUBBLE",
    "PINGPONG",
    # "SINGING",
    # "GHOST",
    # "BLOOD",
    "BAT",
    "TOY",
    "STIR"
]
TRICK_TIMES = {
    "BUBBLE": 10,
    "PINGPONG": 5,
    "BAT": 10,
    "TOY": 5,
    "STIR": 10
}
# GPIO PINS
TREAT_BUTTON_PIN = 14  
TRICK_BUTTON_PIN = 18
# GHOST_BUTTON_PIN = 0
TREAT_LED_PIN = 15
TRICK_LED_PIN = 22
TREAT_MOTOR_FORWARD_PIN = 17
TREAT_MOTOR_BACKWARD_PIN = 27
STIR_MOTOR_FORWARD_PIN = 7
STIR_MOTOR_BACKWARD_PIN = 8
SINGING_SWITCH = 6
PING_PONG_PIN = 13
BUBBLE_SWITCH = 19
BUBBLE_SWITCH_2 = 26
LIGHTS_PIN_ON = 2
LIGHTS_PIN_OFF = 3
BAT_PIN = 23
TOY_PIN = 24

# Trick or Treat object to handle devices
class TrickOrTreat():
    def __init__(self, sphero_mac: str):
        self.running = False
        self.current_trick = None
        self.trick_end_time = time.time()
        self.treat_queue = queue.Queue()
        # Setup motors
        self.treat_motor = Motor(forward=TREAT_MOTOR_FORWARD_PIN,
                                 backward=TREAT_MOTOR_BACKWARD_PIN)
        self.treat_motor.stop()
        self.stir_motor = Motor(forward=STIR_MOTOR_FORWARD_PIN,
                                backward=STIR_MOTOR_BACKWARD_PIN)
        self.stir_motor.stop()
        # Setup buttons
        # self.ghost_button = Button(GHOST_BUTTON_PIN)
        self.treat_button = Button(TREAT_BUTTON_PIN)
        self.trick_button = Button(TRICK_BUTTON_PIN)
        self.prev_trick_button = False
        self.prev_treat_button = False
        # Setup LEDs
        self.treat_led = LED(TREAT_LED_PIN)
        self.trick_led = LED(TRICK_LED_PIN)
        # Setup continuous tricks
        # self.time_since_bird = time.time()
        # Setup sphero ball
        if sphero_mac:
            self.sphero = sphero_mini.sphero_mini(sphero_mac)
            self.time_since_eye = time.time()
        else:
            self.sphero = None
            self.time_since_eye = None
        self.tricks = cycle(TRICKS)
        # Setup other tricks
        # self.ghost_on = DigitalOutputDevice(GHOST_PIN_ON, active_high=False)
        # self.ghost_off = DigitalOutputDevice(GHOST_PIN_OFF, active_high=False)
        # self.ghost = DigitalOutputDevice(GHOST_PIN, active_high=False)
        self.bat = DigitalOutputDevice(BAT_PIN, active_high=False)
        self.toy = DigitalOutputDevice(TOY_PIN, active_high=False)
        self.ping_pong = DigitalOutputDevice(PING_PONG_PIN, active_high=False)
        self.lights_on = DigitalOutputDevice(LIGHTS_PIN_ON, active_high=False)
        self.lights_off = DigitalOutputDevice(LIGHTS_PIN_OFF, active_high=False)
        # Start by turning on the lights
        self.lights_on.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.lights_on.off()
        # self.bird = DigitalOutputDevice(BIRD_PIN, active_high=False)
        # self.singing = DigitalOutputDevice(SINGING_SWITCH, active_high=False)
        self.bubble_switch = DigitalOutputDevice(BUBBLE_SWITCH, active_high=False)
        self.bubble_switch_2 = DigitalOutputDevice(BUBBLE_SWITCH_2, active_high=False)
        # Setup tricks threads
        self.trick_thread = threading.Thread(target=self._handle_tricks)
        self.treat_thread = threading.Thread(target=self._handle_treats)
        self.continuous_trick_thread = \
            threading.Thread(target=self._handle_continuous_tricks)
        
    def _handle_continuous_tricks(self):
        while self.running:
            # Run continuous tricks
            if self.sphero:
                if (time.time() - self.time_since_eye) > EYE_TIME:
                    print("running sphero trick")
                    self._sphero_trick()
                    self.time_since_eye = time.time()
            # if (time.time() - self.time_since_bird) > BIRD_TIME:
            #     self._bird_trick()
            #     self.time_since_bird = time.time()

    def _handle_treats(self):
        while self.running:
            treat = self.treat_queue.get()
            if treat == "CANDY":
                self._treat()
        
    def _handle_tricks(self):
        while self.running:
            if time.time() < self.trick_end_time:
                self.trick_led.on()
            else:
                self.trick_led.off()
            trick = self.current_trick
            if trick is not None:
                print(f"trick button pressed. Performing trick: {trick}")
            if trick == "BUBBLE":
                self._bubble_trick()
            elif trick == "PINGPONG":
                self._ping_pong_trick()
            elif trick == "TOY":
                self._toy_trick()
            elif trick == "BAT":
                self._bat_trick()
            elif trick == "STIR":
                self._stir_trick()
            elif trick is None:
                time.sleep(0.01)
            else:
                print(f"Unknown trick: {trick}")
            
    def _bubble_trick(self):
        self.bubble_switch.on()
        self.bubble_switch_2.on()
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        self.bubble_switch.off()
        self.bubble_switch_2.off()

    def _ghost_trick(self):
        self.ghost.on()
        self.ghost_on.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.ghost_on.off()
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        # Press on button again
        self.ghost_on.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.ghost_on.off()
        time.sleep(BUTTON_PRESS_DELAY)
        # Then press off button again
        self.ghost_off.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.ghost_off.off()
        self.ghost.off()

    def _ping_pong_trick(self):
        self.ping_pong.on()
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        self.ping_pong.off()

    def _toy_trick(self):
        self.toy.on()
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        self.toy.off()

    def _bat_trick(self):
        self.bat.on()
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        self.bat.off()

    def _lights_trick(self):
        while (time.time() - self.trick_end_time) < 0:
            self.lights_off.on()
            time.sleep(BUTTON_PRESS_DELAY)
            self.lights_off.off()
            time.sleep(LIGHTS_TIME)
            self.lights_on.on()
            time.sleep(BUTTON_PRESS_DELAY)
            self.lights_on.off()
            time.sleep(LIGHTS_TIME)

    def _singing_trick(self):
        # Press button on singing toy
        self.singing.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.singing.off()
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        self.singing.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.singing.off()
    
    def _stir_trick(self):
        self.stir_motor.forward(STIR_SPEED)
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        self.stir_motor.stop()
    
    def _blood_trick(self):
        self.blood_motor.forward(BLOOD_SPEED)
        while (time.time() - self.trick_end_time) < 0:
            time.sleep(0.01)
        self.blood_motor.stop()
        
    def _bird_trick(self):
        # Make bird flap wings
        self.bird.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.bird.off()
        time.sleep(BIRD_TIME)
        # Make bird stop flapping
        self.bird.on()
        time.sleep(BUTTON_PRESS_DELAY)
        self.bird.off()

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
        self.treat_motor.forward(CANDY_SPEED)
        time.sleep(TREAT_TIME)
        self.treat_motor.backward()
        time.sleep(TREAT_TIME)
        self.treat_motor.forward()
        time.sleep(TREAT_TIME)
        time.sleep(TREAT_TIME)
        self.treat_motor.stop()
        self.treat_led.off()
    
    def run(self):
        self.running = True
        # Start threads
        self.continuous_trick_thread.start()
        self.trick_thread.start()
        self.treat_thread.start()
        while self.running:
            treat_pressed = self.prev_treat_button and not self.treat_button.is_pressed
            trick_pressed = self.prev_trick_button and not self.trick_button.is_pressed
            self.prev_treat_button = self.treat_button.is_pressed
            self.prev_trick_button = self.trick_button.is_pressed
            # print(f"prev: {self.prev_treat_button}, curr: {self.treat_button.is_pressed}")
            if time.time() > self.trick_end_time:
                self.current_trick = None
            if treat_pressed:
                logging.info("treat")
                self.treat_queue.put("CANDY")
            elif trick_pressed:
                if not self.current_trick:
                    logging.info("trick")
                    self.current_trick = next(self.tricks)
                    self.trick_end_time = time.time() + TRICK_TIMES[self.current_trick]
                else:
                    self.current_trick = None
                    self.trick_end_time = time.time()
            else:
                # Don't run too fast
                time.sleep(0.01)
        print("end of run")

    def stop(self):
        self.running = False
        if self.sphero is not None:
            self.sphero.disconnect()
        print("end of stop")

if __name__ == '__main__':
    # EB:B6:31:82:7C:F0
    sphero_mac = sys.argv[1]
    # sphero_mac = "EB:B6:31:82:7C:F0"
    print("Welcome trick or treaters")
    trick_or_treat = TrickOrTreat(sphero_mac)
    # trick_or_treat = TrickOrTreat("")
    try:
        trick_or_treat.run()
    except KeyboardInterrupt:
        trick_or_treat.stop()
    print("\ngoodbye")


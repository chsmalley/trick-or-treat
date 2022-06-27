import sys
from gpiozero import Motor, Button, LED
import time
import sphero_mini

# CONSTANTS
CANDY_TIME = 2
BUBBLE_TIME = 2
ROLL_TIME = 10
ROLL_STEP_TIME = 0.5

# Trick or Treat object to handle devices
class TrickOrTreat():
    def __init__(self, sphero_mac: str):
        self.running = False
        # Setup motors
        self.candy_motor = Motor(forward=4, backward=14)
        self.bubble_motor = Motor(forward=17, backward=27)
        # Setup buttons
        self.candy_button = Button(2)
        self.bubble_button = Button(3)
        # Setup LEDs
        self.candy_led = LED(20)
        self.bubble_led = LED(21)
        # Setup sphero ball
        self.sphero = sphero_mini.sphero_mini(sphero_mac)
        # Setup other tricks

    def trick_sphero(self):
        start_time = time.time()
        self.sphero.setLEDColor(red=255, green=0, blue=0)
        while(time.time() - start_time < ROLL_TIME):
            self.sphero.roll(100, 45)
            self.sphero.wait(ROLL_STEP_TIME)
            self.sphero.roll(0, 0)
            self.sphero.wait(1)
        self.sphero.setLEDColor(red=0, green=0, blue=255)
    
    def run(self):
        self.running = True
        while True:
            if self.candy_button.is_pressed:
                print("candy button pressed")
                self.candy_motor.forward()
                self.candy_led.on()
                time.sleep(CANDY_TIME)
                self.candy_motor.stop()
                self.candy_led.off()
            elif self.bubble_button.is_pressed:
                print("bubble button pressed")
                self.bubble_motor.forward()
                self.bubble_led.on()
                time.sleep(BUBBLE_TIME)
                self.bubble_motor.stop()
                self.bubble_led.off()
            else:
                # Don't run too fast
                time.sleep(0.01)

    def stop(self):
        pass

if __name__ == '__main__':
    print("Welcome trick or treaters")
    trick_or_treat = TrickOrTreat()
    try:
        trick_or_treat.run()
    except KeyboardInterrupt:
        trick_or_treat.stop()
    print("goodbye")


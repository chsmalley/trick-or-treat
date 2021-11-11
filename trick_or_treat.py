import sys
from gpiozero import Motor, Button
import time

CANDY_TIME = 2
BUBBLE_TIME = 2

def trick_or_treat():
    # Setup motors
    candy_motor = Motor(forward=4, backward=14)
    bubble_motor = Motor(forward=17, backward=27)
    # Setup buttons
    candy_button = Button(2)
    bubble_button = Button(3)
    # Setup LEDs
    candy_led = LED(20)
    bubble_led = LED(21)
    # main loop
    try:
        while True:
            if candy_button.is_pressed:
                print("candy button pressed")
                candy_motor.forward()
                candy_led.on()
                time.sleep(CANDY_TIME)
                candy_motor.stop()
                candy_led.off()
            elif bubble_button.is_pressed:
                print("bubble button pressed")
                bubble_motor.forward()
                bubble_led.on()
                time.sleep(BUBBLE_TIME)
                bubble_motor.stop()
                bubble_led.off()
            else:
                # Don't run too fast
                time.sleep(0.01)
    except KeyboardInterrupt:
        candy_motor.stop()
        bubble_motor.stop()


if __name__ == '__main__':
    print("Welcome trick or treaters")
    trick_or_treat()
    print("goodbye")

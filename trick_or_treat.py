import sys
from gpiozero import Motor, Button, LED
import time

CANDY_TIME = 4
BUBBLE_TIME = 1.0
CANDY_SPEED = 0.9
BUBBLE_SPEED = 1.0

def trick_or_treat():
    # Setup motors
    candy_motor = Motor(forward=23, backward=24)
    bubble_motor = Motor(forward=27, backward=17)
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
                candy_led.on()
                for _ in range(CANDY_TIME):
                    candy_motor.forward(CANDY_SPEED)
                    time.sleep(1)
                    candy_motor.backward(CANDY_SPEED)
                    time.sleep(0.1)
                candy_motor.stop()
                candy_led.off()
            elif bubble_button.is_pressed:
                print("bubble button pressed")
                bubble_led.on()
                bubble_motor.backward(BUBBLE_SPEED)
                time.sleep(BUBBLE_TIME)
                bubble_motor.forward(BUBBLE_SPEED)
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

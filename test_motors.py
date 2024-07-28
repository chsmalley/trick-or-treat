from gpiozero import Motor
import keyboard
import time

# Define GPIO pins for motors
MOTOR1_FORWARD_PIN = 17
MOTOR1_BACKWARD_PIN = 27
MOTOR2_FORWARD_PIN = 23
MOTOR2_BACKWARD_PIN = 24

def set_motor_speed(motor, speed):
    """Set the speed of the motor (0.0 to 1.0)."""
    if speed > 0 and speed <= 1:
        motor.forward(speed)
    elif speed >= -1 and speed < 0:
        motor.backward(abs(speed))
    else:
        print("Speed must be between -1.0 and 1.0")

def main():
    # Create Motor objects
    motor1 = Motor(forward=MOTOR1_FORWARD_PIN, backward=MOTOR1_BACKWARD_PIN)
    motor2 = Motor(forward=MOTOR2_FORWARD_PIN, backward=MOTOR2_BACKWARD_PIN)
    print("Control Motor Speeds:")
    print("Press number to select motor")
    print("Press up arrow to increase speed")
    print("Press down arrow to decrease speed")

    motor1_speed = 0.0
    motor2_speed = 0.0
    current_motor = None

    try:
        while True:
            if keyboard.is_pressed("1"):
                current_motor = motor1
            if keyboard.is_pressed("2"):
                current_motor = motor2
            if current_motor:
                if keyboard.is_pressed('up'):
                    if current_motor == motor1:
                        motor1_speed = min(motor1_speed + 0.1, 1.0)
                        print(f"Motor 1 Speed: {motor1_speed:.1f}")
                        set_motor_speed(motor2, motor2_speed)
                    elif current_motor == motor2:
                        motor2_speed = min(motor2_speed + 0.1, 1.0)
                        print(f"Motor 2 Speed: {motor2_speed:.1f}")
                        set_motor_speed(motor2, motor2_speed)
                    else:
                        print("no motor selected")
                    time.sleep(0.1)  # Debounce delay
                if keyboard.is_pressed('down'):
                    if current_motor == motor1:
                        motor1_speed = max(motor1_speed - 0.1, -1.0)
                        print(f"Motor 1 Speed: {motor1_speed:.1f}")
                        set_motor_speed(motor2, motor2_speed)
                    elif current_motor == motor2:
                        motor2_speed = max(motor2_speed - 0.1, -1.0)
                        print(f"Motor 2 Speed: {motor2_speed:.1f}")
                        set_motor_speed(motor2, motor2_speed)
                    else:
                        print("no motor selected")
                    time.sleep(0.1)  # Debounce delay

            if keyboard.is_pressed('q'):
                print("Quitting...")
                break

    except KeyboardInterrupt:
        print("Program interrupted.")

    finally:
        # Stop motors and cleanup
        motor1.off()
        motor2.off()

if __name__ == "__main__":
    main()

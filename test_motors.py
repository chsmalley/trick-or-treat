from gpiozero import Motor
import time

# Define GPIO pins for motors
MOTOR1_FORWARD_PIN = 20
MOTOR1_BACKWARD_PIN = 21
MOTOR2_FORWARD_PIN = 2
MOTOR2_BACKWARD_PIN = 3

def set_motor_speed(motor, speed):
    """Set the speed of the motor (0.0 to 1.0)."""
    if speed >= -1 and speed <= 1:
        if speed >= 0:
            motor.forward(speed)
        else:
            motor.backward(abs(speed))
    else:
        print("Speed must be between -1.0 and 1.0")

def main():
    # Create Motor objects
    motor1 = Motor(forward=MOTOR1_FORWARD_PIN, backward=MOTOR1_BACKWARD_PIN)
    motor2 = Motor(forward=MOTOR2_FORWARD_PIN, backward=MOTOR2_BACKWARD_PIN)
    print("Control Motor Speeds:")
    print("Enter the motor and then the speed")
    print("example: a 0.8")

    motor1_speed = 0.0
    motor2_speed = 0.0
    current_motor = None

    try:
        while True:
            user_input = input("enter command: ").strip().split()
            motor, speed = user_input
            speed = float(speed)
            print(f"motor: {motor}")
            print(f"speed: {speed}")
            if motor == "a":
                current_motor = motor1
            if motor == "b":
                current_motor = motor2
            if current_motor:
                if current_motor == motor1:
                    motor1_speed = speed
                    print(f"Motor A Speed: {motor1_speed:.1f}")
                    set_motor_speed(motor2, motor2_speed)
                elif current_motor == motor2:
                    motor2_speed = speed
                    print(f"Motor B Speed: {motor2_speed:.1f}")
                    set_motor_speed(motor2, motor2_speed)
                else:
                    print("no motor selected")
                time.sleep(0.1)  # Debounce delay

            if user_input == "q":
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

import serial
import json

# Change COM port as needed (e.g., 'COM3' on Windows or '/dev/ttyUSB0' on Linux)
ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith('{') and line.endswith('}'):
            data = json.loads(line)
            print("Received:", data)
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
    except KeyboardInterrupt:
        print("Exiting...")
        break

ser.close()

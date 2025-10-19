import serial
import json

KNOWN_WANDS = {
    56705: "Camilla",
    60929: "Juliet"
}


ser = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    try:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith('{') and line.endswith('}'):
            data = json.loads(line)
            print("Received:", data)
            if data["address"] in KNOWN_WANDS.keys():
                print(f"Hello {KNOWN_WANDS[data["address"]]}")
    except json.JSONDecodeError as e:
        print("JSON decode error:", e)
    except KeyboardInterrupt:
        print("Exiting...")
        break

ser.close()

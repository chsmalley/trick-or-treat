import socket

# Define the port to listen on.
# This port should match the port used by the sender of the broadcast messages.
UDP_PORT = 12345 
UDP_IP = "0.0.0.0"

def receive_broadcast():
    # Create a UDP socket.
    # socket.AF_INET specifies the address family (IPv4).
    # socket.SOCK_DGRAM specifies the socket type (UDP).
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Allow reuse of the address and port.
    # This is useful when restarting the script quickly or if multiple processes need to bind to the same address/port.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the specified port on all available interfaces.
    # The empty string '' as the IP address means the socket will listen on all network interfaces.
    sock.bind((UDP_IP, UDP_PORT))
    # sock.bind(('', UDP_PORT))

    print(f"Listening for UDP broadcast messages on port {UDP_PORT}...")

    while True:
        try:
            # Receive data from the socket.
            # 1024 is the buffer size, meaning it can receive up to 1024 bytes at a time.
            # data will contain the received message in bytes.
            # addr will contain a tuple (IP_address, port) of the sender.
            data, addr = sock.recvfrom(1024) 

            # Decode the received bytes into a string.
            message = data.decode('utf-8') 

            print(f"Received message: '{message}' from {addr}")

        except KeyboardInterrupt:
            print("\nExiting broadcast receiver.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    sock.close()

if __name__ == "__main__":
    receive_broadcast()

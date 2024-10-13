import socket
from time import sleep

TCP_IP = '10.30.37.120'  # Target IP address
TCP_PORT = 14            # Target port
BUFFER_SIZE = 1024       # Buffer size for receiving data

# Create a TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    s.connect((TCP_IP, TCP_PORT))
    print(f"Connected to {TCP_IP}:{TCP_PORT}")

    while True:
        # Receive data from the server
        data = s.recv(BUFFER_SIZE).decode(encoding="utf-8", errors="ignore")
        
        if not data:  # If no data is received, the connection may be closed
            print("No data received, connection might be closed.")
            break

        # Print the received data
        print(f"Received data: {data}")

        # Sleep to avoid overwhelming the server (adjust the sleep time as needed)
        sleep(1)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the socket when done
    print("Closing connection.")
    s.close()
    
    
    
    
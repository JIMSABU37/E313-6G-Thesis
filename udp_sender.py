import socket
import time

# Point this directly at your Pi's IP address
UDP_IP = "192.168.1.83"
UDP_PORT = 5005

print(f"[*] URLLC Sender Online: Firing fast data at {UDP_IP}:{UDP_PORT}...")

# Initialize the connectionless UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

counter = 1
while True:
    message = f"URLLC Safety Message #{counter} - Brakes Applied!"
    
    # Fire the packet over the network
    sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    print(f"[Sent] {message}")
    
    counter += 1
    time.sleep(1) # Firing 1 message per second so it is readable
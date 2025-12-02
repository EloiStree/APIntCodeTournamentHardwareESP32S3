import socket
import time

# Target IP: replace with your CircuitPython board's IP  http://192.168.178.67:5000
TARGET_IP = "192.168.178.67"   # Example, change to your board's IP
TARGET_PORT = 3615

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Sending UDP packets to {TARGET_IP}:{TARGET_PORT}...")

def send_package_iid(int_value:int):
    #send litte-endian 4 byte integer
    byte_array = int_value.to_bytes(4, byteorder='little')
    sock.sendto(byte_array, (TARGET_IP, TARGET_PORT))

counter = 0
while True:
    message = f"Packet #{counter}".encode("utf-8")
    sock.sendto(message, (TARGET_IP, TARGET_PORT))
    print(f"Sent: {message}")
    counter += 1
    time.sleep(1)  # send one packet per second

    note = counter % 128
    print(f"Sending MIDI Note On for note {note}")
    send_package_iid(note+1600)  # Note On on channel 1
    time.sleep(0.5)
    print(f"Sending MIDI Note Off for note {note}") 
    send_package_iid(note+2600)  # Note Off on channel 1



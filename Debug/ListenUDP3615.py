import socket

# Create UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('0.0.0.0', 3617))

print('Listening on UDP port 3615...')

while True:
    try:
        data, addr = udp_socket.recvfrom(1024)
        print(f'Received from {addr}: {data}')
    except KeyboardInterrupt:
        break

udp_socket.close()

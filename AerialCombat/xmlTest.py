import socket
import sys

UDP_IP = "localhost"
UDP_PORT = 5500
address = (UDP_IP, UDP_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
print('connected to ')

while True:
    data, addr = sock.recvfrom(1024)
    print('data',data)

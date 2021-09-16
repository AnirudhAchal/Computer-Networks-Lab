import socket
import threading

# Constants
HEADER = 64
PORT = 5050
SERVER = '192.168.1.225'
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM

# Server Socket
client = socket.socket(SOCKET_FAMILY, SOCKET_PROTOCOL)
client.connect(ADDRESS)


def receive_message():
    header = client.recv(HEADER).decode(FORMAT)
    if header:
        server_message_length = int(header)
        if server_message_length > 0:
            server_message = client.recv(server_message_length).decode(FORMAT)
            print(f'[SERVER MESSAGE] {server_message}')


def start_client():
    while True:
        receive_message()


def main():
    start_client()


main()



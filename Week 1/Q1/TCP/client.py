import socket

# Constants
HEADER = 64
PORT = 5050
SERVER = input('Server IP Address: ')
SERVER_ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM


class Client:
    def __init__(self, socket_family, socket_protocol, server_address):
        # Client Socket
        self.client = socket.socket(socket_family, socket_protocol)
        self.client.connect(server_address)

    def receive_message(self):
        header = self.client.recv(HEADER).decode(FORMAT)
        if header:
            server_message_length = int(header)
            if server_message_length > 0:
                server_message = self.client.recv(server_message_length).decode(FORMAT)
                print(f'[SERVER MESSAGE] {server_message}')

    def start(self):
        while True:
            self.receive_message()


def main():
    client = Client(SOCKET_FAMILY, SOCKET_PROTOCOL, SERVER_ADDRESS)
    client.start()


main()



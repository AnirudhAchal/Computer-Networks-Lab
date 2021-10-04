import socket
import time

# Constants
HEADER = 64
PORT = 5000
SERVER = input('Server IP Address: ')
SERVER_ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_DGRAM


class Client:
    def __init__(self, socket_family, socket_protocol, server_address):
        # Client Socket
        self.client = socket.socket(socket_family, socket_protocol)
        self.server_address = server_address

    @staticmethod
    def _make_header(message):
        message_length = len(message)

        # Encoding the header
        header = str(message_length).encode(FORMAT)

        # Pad the header
        header = b' ' * (HEADER - len(header)) + header

        return header

    def send_message(self, message):
        self.client.sendto(self._make_header(message), self.server_address)
        self.client.sendto(message.encode(FORMAT), self.server_address)

    def receive_message(self):
        header, address = self.client.recvfrom(HEADER)

        if header:
            server_message_length = int(header.decode(FORMAT))
            if server_message_length > 0:
                server_message, address = self.client.recvfrom(server_message_length)
                server_message = server_message.decode(FORMAT)

                print(f'[SERVER MESSAGE] {server_message}')

    def start(self):
        while True:
            self.send_message('Connection request')
            self.receive_message()

            time.sleep(30)


def main():
    client = Client(SOCKET_FAMILY, SOCKET_PROTOCOL, SERVER_ADDRESS)
    client.start()


main()



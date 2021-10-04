import socket
import threading

# Constants
HEADER = 64
PORT = 5000
SERVER = input('Server IP Address: ')
SERVER_ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_DGRAM


class Client:
    def __init__(self, socket_family, socket_protocol, server_address, username):
        # Client Socket
        self.client = socket.socket(socket_family, socket_protocol)
        self.server_address = server_address
        self.username = username

        self.send_message(username)

    @staticmethod
    def _make_header(message):
        message_length = len(message)

        # Encoding the header
        header = str(message_length).encode(FORMAT)

        # Pad the header
        header = b' ' * (HEADER - len(header)) + header

        return header

    def receive_message(self):
        while True:
            try:
                header, address = self.client.recvfrom(HEADER)

                if header:
                    server_message_length = int(header.decode(FORMAT))

                    if server_message_length > 0:
                        server_message, address = self.client.recvfrom(server_message_length)
                        server_message = server_message.decode(FORMAT)
                        print(f'{server_message}')
            except Exception as e:
                print(e, f'[CONNECTION CLOSED] server disconnected')
                return

    def send_message(self, message):
        self.client.sendto(self._make_header(message), self.server_address)
        self.client.sendto(message.encode(FORMAT), self.server_address)

    def handle_send_message(self):
        while True:
            try:
                self.send_message(input())
            except Exception as e:
                print(e, f'[CONNECTION CLOSED] server disconnected')
                return

    def start(self):
        # Set Receiving Thread
        receiving_thread = threading.Thread(target=self.receive_message)
        receiving_thread.start()

        # Set Sending Thread
        sending_thread = threading.Thread(target=self.handle_send_message)
        sending_thread.start()

    def get_date(self):
        self.send_message('current_date?')


def main():
    username = input('Username: ')

    client = Client(SOCKET_FAMILY, SOCKET_PROTOCOL, SERVER_ADDRESS, username)
    client.start()


main()

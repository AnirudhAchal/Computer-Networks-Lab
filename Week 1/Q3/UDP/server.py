import socket
import threading
import datetime

# Constants
HEADER = 64
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_DGRAM
LOCK = threading.Lock()


class Server:
    def __init__(self, socket_family, socket_protocol, address):
        # Server Socket
        self.server = socket.socket(socket_family, socket_protocol)
        self.server.bind(address)
        self.client_address = None

    @staticmethod
    def _make_header(message):
        message_length = len(message)

        # Encoding the header
        header = str(message_length).encode(FORMAT)

        # Pad the header
        header = b' ' * (HEADER - len(header)) + header

        return header

    def send_message(self, message, address):
        self.server.sendto(self._make_header(message), address)
        self.server.sendto(message.encode(FORMAT), address)

    def receive_message(self):
        while True:
            header, address = self.server.recvfrom(HEADER)
            self.client_address = address

            if header:
                client_message_length = int(header.decode(FORMAT))
                if client_message_length > 0:
                    client_message, address = self.server.recvfrom(client_message_length)
                    client_message = client_message.decode(FORMAT)

                    print(f'[NEW MESSAGE] {address} {client_message}')

    def handle_send_message(self):
        while self.client_address is None:
            # We cannot send messages until a we know the client address
            pass

        while True:
            try:
                self.send_message(input(), self.client_address)
                print(f'[MESSAGE SENT] {self.client_address}')
            except Exception as e:
                print(e, '[Client lost] cannot send message')

    def start(self):
        print(f'[STARTING] server is starting on {SERVER}...')

        # Set receiving thread
        receiving_thread = threading.Thread(target=self.receive_message)
        receiving_thread.start()

        # Set sending thread
        sending_thread = threading.Thread(target=self.handle_send_message)
        sending_thread.start()


def main():
    server = Server(SOCKET_FAMILY, SOCKET_PROTOCOL, ADDRESS)
    server.start()


main()

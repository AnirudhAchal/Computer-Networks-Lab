import socket
import time

# Constants
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM


class Server:
    def __init__(self, socket_family, socket_protocol, address):
        # Server Socket
        self.server = socket.socket(socket_family, socket_protocol)
        self.server.bind(address)

    @staticmethod
    def _make_header(message):
        message_length = len(message)

        # Encoding the header
        header = str(message_length).encode(FORMAT)

        # Pad the header
        header = b' ' * (HEADER - len(header)) + header

        return header

    def greet_client(self, connection, address):
        print(f'[NEW CONNECTION] {address} connected')

        while True:
            try:
                greeting_message = f'You are connected to the server at {ADDRESS}'
                connection.send(self._make_header(greeting_message))
                connection.send(greeting_message.encode(FORMAT))
            except ConnectionResetError:
                connection.close()
                print(f'[CONNECTION CLOSED] {address} disconnected')
                return

            time.sleep(30)

    def start(self):
        print(f'[STARTING] server is starting...')

        self.server.listen()
        print(f'[LISTENING] server is listening on {SERVER}...')

        while True:
            connection, address = self.server.accept()
            self.greet_client(connection, address)


def main():
    server = Server(SOCKET_FAMILY, SOCKET_PROTOCOL, ADDRESS)
    server.start()


main()

import socket

# Constants
HEADER = 64
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_DGRAM


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

    def greet_client(self):
        header, address = self.server.recvfrom(HEADER)

        if header:
            client_message_length = int(header.decode(FORMAT))
            if client_message_length > 0:
                client_message, address = self.server.recvfrom(client_message_length)
                client_message = client_message.decode(FORMAT)

                print(f'[NEW MESSAGE] {address} {client_message}')

                greeting_message = f'You are connected to the server at {ADDRESS}'
                self.server.sendto(self._make_header(greeting_message), address)
                self.server.sendto(greeting_message.encode(FORMAT), address)

    def start(self):
        print(f'[STARTING] server is starting on {SERVER}...')

        while True:
            self.greet_client()


def main():
    server = Server(SOCKET_FAMILY, SOCKET_PROTOCOL, ADDRESS)
    server.start()


main()

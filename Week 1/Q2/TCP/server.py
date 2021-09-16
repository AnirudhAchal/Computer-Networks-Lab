import socket
import threading
import datetime

# Constants
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM
LOCK = threading.Lock()


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

    def send_message(self, connection, message):
        with LOCK:
            connection.send(self._make_header(message))
            connection.send(message.encode(FORMAT))

    def handle_client_message(self, connection, address, client_message):
        print(f'[{address} MESSAGE] {client_message}')
        if client_message == 'current_date?':
            current_date = str(datetime.date.today())
            self.send_message(connection, current_date)

    def receive_message(self, connection, address):
        while connection:
            try:
                header = connection.recv(HEADER).decode(FORMAT)
                if header:
                    client_message_length = int(header)
                    client_message = connection.recv(client_message_length).decode(FORMAT)
                    self.handle_client_message(connection, address, client_message)
            except ConnectionResetError:
                connection.close()
                print(f'[CONNECTION CLOSED] {address} disconnected')
                return

    def handle_client(self, connection, address):
        print(f'[NEW CONNECTION] {address} connected')

        try:
            greeting_message = f'You are connected to the server at {ADDRESS}'
            self.send_message(connection, greeting_message)
        except ConnectionResetError:
            connection.close()
            print(f'[CONNECTION CLOSED] {address} disconnected')
            return

        # Set receiving thread
        receiving_thread = threading.Thread(target=self.receive_message, args=(connection, address))
        receiving_thread.start()

    def start(self):
        print(f'[STARTING] server is starting...')

        self.server.listen()
        print(f'[LISTENING] server is listening on {SERVER}...')

        while True:
            connection, address = self.server.accept()
            self.handle_client(connection, address)


def main():
    server = Server(SOCKET_FAMILY, SOCKET_PROTOCOL, ADDRESS)
    server.start()


main()

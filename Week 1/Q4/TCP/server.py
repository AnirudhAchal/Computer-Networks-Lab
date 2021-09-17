import socket
import threading
import time

# Constants
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM
MESSAGE_LOCK = threading.Lock()
SEND_LOCK = threading.Lock()


class Server:
    def __init__(self, socket_family, socket_protocol, address):
        # Server Socket
        self.server = socket.socket(socket_family, socket_protocol)
        self.server.bind(address)
        self.connections = []
        self.addresses = []
        self.new_messages = []
        self.usernames = {}

    @staticmethod
    def _make_header(message):
        message_length = len(message)

        # Encoding the header
        header = str(message_length).encode(FORMAT)

        # Pad the header
        header = b' ' * (HEADER - len(header)) + header

        return header

    def send_message(self, connection, message):
        with SEND_LOCK:
            connection.send(self._make_header(message))
            connection.send(message.encode(FORMAT))

    def handle_receive_message(self, connection, address):
        while True:
            try:
                header = connection.recv(HEADER).decode(FORMAT)
                if header:
                    client_message_length = int(header)
                    with MESSAGE_LOCK:
                        client_message = connection.recv(client_message_length).decode(FORMAT)
                        print(f'[MESSAGE RECEIVED] {address} {self.usernames[address]} {client_message}')
                        self.new_messages.append({
                            'connection': connection,
                            'address': address,
                            'message': f'[{self.usernames[address]}] {client_message}'
                        })
            except ConnectionResetError:
                print(f'[CONNECTION LOST] {address} {self.usernames[address]} disconnected')
                return

    def handle_send_message(self):
        while True:
            with MESSAGE_LOCK:
                for new_message in self.new_messages:
                    for connection, address in zip(self.connections, self.addresses):
                        if connection != new_message['connection']:
                            try:
                                self.send_message(connection, new_message['message'])
                                print(f'[MESSAGE SENT] {address} {self.usernames[address]}')
                            except ConnectionResetError:
                                print(f'[CONNECTION LOST] {address} {self.usernames[address]} disconnected')
                self.new_messages.clear()

    def greet_client(self, connection, address):
        try:
            greeting_message = f'You are connected to the server at {ADDRESS}'
            self.send_message(connection, greeting_message)
            header = None
            while header is None:
                header = connection.recv(HEADER).decode(FORMAT)
            username_length = int(header)
            with MESSAGE_LOCK:
                username = connection.recv(username_length).decode(FORMAT)
                self.usernames[address] = username
                print(f'{address} {username} has joined the chat')
                self.new_messages.append({
                    'connection': connection,
                    'address': address,
                    'message': f'[{address}] {username} has joined the chat'
                })
        except ConnectionResetError:
            print(f'[CONNECTION CLOSED] {address} disconnected')
            self.connections.remove(connection)
            self.addresses.remove(address)
            self.usernames[address] = ""
            connection.close()
            return

    def handle_client(self, connection, address):
        self.connections.append(connection)
        self.addresses.append(address)
        print(f'[NEW CONNECTION] {address} connected')

        self.greet_client(connection, address)

        # Set receiving thread
        receiving_thread = threading.Thread(target=self.handle_receive_message, args=(connection, address))
        receiving_thread.start()

        receiving_thread.join()

        self.connections.remove(connection)
        self.addresses.remove(address)
        self.usernames[address] = ""
        print(f'[CONNECTION CLOSED] {address} disconnected')
        connection.close()

    def start(self):
        print(f'[STARTING] server is starting...')

        self.server.listen()
        print(f'[LISTENING] server is listening on {SERVER}...')

        # Set sending thread
        sending_thread = threading.Thread(target=self.handle_send_message)
        sending_thread.start()

        while True:
            connection, address = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()


def main():
    server = Server(SOCKET_FAMILY, SOCKET_PROTOCOL, ADDRESS)
    server.start()


main()

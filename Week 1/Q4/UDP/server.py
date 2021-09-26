import socket
import threading

# Constants
HEADER = 64
PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_DGRAM
MESSAGE_LOCK = threading.Lock()


class Server:
    def __init__(self, socket_family, socket_protocol, address):
        # Server Socket
        self.server = socket.socket(socket_family, socket_protocol)
        self.server.bind(address)
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

    def send_message(self, message, address):
        self.server.sendto(self._make_header(message), address)
        self.server.sendto(message.encode(FORMAT), address)

    def receive_message(self):
        try:
            while True:
                header, address = self.server.recvfrom(HEADER)

                if header:
                    if address not in self.addresses:
                        username_length = int(header.decode(FORMAT))

                        with MESSAGE_LOCK:
                            username, address = self.server.recvfrom(username_length)
                            username = username.decode(FORMAT)
                            self.usernames[address] = username

                            print(f'{address} {username} has joined the chat')
                            self.new_messages.append({
                                'address': address,
                                'message': f'[{address}] {username} has joined the chat'
                            })

                        self.addresses.append(address)
                    else:
                        client_message_length = int(header.decode(FORMAT))
                        if client_message_length > 0:
                            with MESSAGE_LOCK:
                                client_message, address = self.server.recvfrom(client_message_length)
                                client_message = client_message.decode(FORMAT)
                                print(f'[MESSAGE RECEIVED] {address} {self.usernames[address]} {client_message}')
                                self.new_messages.append({
                                    'address': address,
                                    'message': f'[{self.usernames[address]}] {client_message}'
                                })
        except ConnectionResetError as e:
            print(f'[CLIENT LOST] {address} disconnected')

    def handle_send_message(self):
        while True:
            with MESSAGE_LOCK:

                for new_message in self.new_messages:
                    for address in self.addresses:
                        if address != new_message['address']:
                            try:
                                self.send_message(new_message['message'], address)
                                print(f'[MESSAGE SENT] {address}')
                            except ConnectionResetError:
                                print(f'[CLIENT LOST] {address} disconnected')

                # Clear old messages
                self.new_messages.clear()

    def start(self):
        print(f'[STARTING] server is starting on {SERVER}...')

        # Set Receiving Thread
        receiving_thread = threading.Thread(target=self.receive_message)
        receiving_thread.start()

        # Set sending thread
        sending_thread = threading.Thread(target=self.handle_send_message)
        sending_thread.start()


def main():
    server = Server(SOCKET_FAMILY, SOCKET_PROTOCOL, ADDRESS)
    server.start()


main()

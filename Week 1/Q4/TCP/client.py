import socket
import threading

# Constants
HEADER = 64
PORT = 5050
SERVER = '192.168.1.225'
SERVER_ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM
LOCK = threading.Lock()


class Client:
    def __init__(self, socket_family, socket_protocol, server_address, username):
        # Client Socket
        self.client = socket.socket(socket_family, socket_protocol)
        self.client.connect(server_address)
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
        # Accept greeting
        try:
            header = self.client.recv(HEADER).decode(FORMAT)
            if header:
                server_message_length = int(header)
                server_message = self.client.recv(server_message_length).decode(FORMAT)
                print(f'[SERVER MESSAGE] {server_message}')
        except Exception as e:
            print(e, f'[CONNECTION CLOSED] server disconnected')
            return

        while True:
            try:
                header = self.client.recv(HEADER).decode(FORMAT)
                if header:
                    server_message_length = int(header)
                    server_message = self.client.recv(server_message_length).decode(FORMAT)
                    print(server_message)
            except Exception as e:
                print(e, f'[CONNECTION CLOSED] server disconnected')
                return

    def send_message(self, message):
        with LOCK:
            self.client.send(self._make_header(message))
            self.client.send(message.encode(FORMAT))

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


def main():
    username = input('Username: ')

    client = Client(SOCKET_FAMILY, SOCKET_PROTOCOL, SERVER_ADDRESS, username)
    client.start()


main()



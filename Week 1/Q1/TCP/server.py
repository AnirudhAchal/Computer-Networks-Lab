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

# Server Socket
server = socket.socket(SOCKET_FAMILY, SOCKET_PROTOCOL)
server.bind(ADDRESS)


def make_header(message):
    message_length = len(message)

    # Encoding the header
    header = str(message_length).encode(FORMAT)

    # Pad the header
    header = b' ' * (HEADER - len(header)) + header

    return header


def handle_client(connection, address):
    print(f'[NEW CONNECTION] {address} connected')

    while True:
        try:
            greeting_message = f'You are connected to the server at {ADDRESS}'
            connection.send(make_header(greeting_message))
            connection.send(greeting_message.encode(FORMAT))
        except ConnectionResetError:
            connection.close()
            print(f'[CONNECTION CLOSE] {address} disconnected')
            return

        time.sleep(30)


def start_server():
    server.listen()
    print(f'[LISTENING] server is listening on {SERVER}...')

    while True:
        connection, address = server.accept()
        handle_client(connection, address)


def main():
    print(f'[STARTING] server is starting...')
    start_server()


main()

import socket
import json

# Constants
HEADER = 64
PORT = 8080
SERVER = input('Server IP Address: ')
BASE_URL = f'http://{SERVER}'
SERVER_ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM


class Client:
    def __init__(self, socket_family, socket_protocol, server_address):
        self.socket_family = socket_family
        self.socket_protocol = socket_protocol
        self.server_address = server_address
        self.client = socket.socket(self.socket_family, self.socket_protocol)

    def request(self, url):
        self.start()

        try:
            self.client.connect(self.server_address)
        except Exception as e:
            print(e, 'Server not available')
            return

        page = url[len(BASE_URL):]
        request = {
            'header': {
                'request-line': f'GET {page} HTTP/1.1',
                'host': SERVER,
                'connection': 'close',
            },
        }

        request = json.dumps(request, indent=4)
        self.client.send(request.encode(FORMAT))

        response = self.client.recv(2048).decode(FORMAT)
        response = json.loads(response)

        print('[SERVER RESPONSE]')
        print((json.dumps(response, indent=4)), '\n')

        print('[HTML]')
        print(response['body'], '\n')

        self.stop()

    def start(self):
        self.client = socket.socket(self.socket_family, self.socket_protocol)

    def stop(self):
        self.client.close()


def main():
    client = Client(SOCKET_FAMILY, SOCKET_PROTOCOL, SERVER_ADDRESS)

    while True:
        url = input(f'URL: http://{SERVER}/')
        url = f'http://{SERVER}/{url}'
        client.request(url)


main()

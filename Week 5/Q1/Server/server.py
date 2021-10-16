import os
import socket
from datetime import date
import json
import ssl

# Constants
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM


class Server:
    def __init__(self, socket_family, socket_protocol, address):
        self.server = socket.socket(socket_family, socket_protocol, 0)
        self.server.bind(address)
        self.html_pages = self.get_html_pages()
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.status_messages = {
            200: 'OK',
            400: 'Invalid Request',
            404: 'Page Not Found'
        }

    @staticmethod
    def get_html_pages():
        html_pages = ['/']
        for file in os.listdir('.'):
            html_pages.append('/' + os.path.splitext(file)[0])
        return html_pages

    def http_response(self, status_code, page=None):
        data = None
        if page:
            if page == '/':
                page = '/index'

            if page[0] == '/':
                page = page[1:]

            with open(f'{page}.html', 'r') as f:
                data = f.read()

        response = {
            'header': {
                'response-line': f'HTTP/1.1 {status_code} {self.status_messages[status_code]}',
                'Date': str(date.today()),
                'connection': 'close',
                'server': 'Windows/10',
                'content-type': 'text/html',
                'content-length': len(data) if data else None
            },
            'body': data
        }

        return response

    def handle_client(self, connection, address):
        request = connection.recv(2048).decode(FORMAT)
        print(f'[REQUEST] ({address})')

        request = json.loads(request)
        print(json.dumps(request, indent=4))

        if request['header']['host'] != SERVER:
            response = self.http_response(status_code=400)
        else:
            request_line = request['header']['request-line']
            request_type, web_page, protocol_version = request_line.split()

            if request_type == 'GET':
                if web_page in self.html_pages:
                    # Return web page
                    response = self.http_response(page=web_page, status_code=200)
                else:
                    # Return Page Not Found
                    response = self.http_response(status_code=404)
            else:
                # Return Invalid Response Type
                response = self.http_response(status_code=400)

        response = json.dumps(response, indent=4)
        connection.send(response.encode(FORMAT))
        connection.close()

    def start(self):
        print(f'[STARTING] server is starting...')

        self.server.listen()
        print(f'[LISTENING] server is listening on {SERVER}...')

        while True:
            with self.context.wrap_socket(self.server, server_side=True) as s_server:
                connection, address = s_server.accept()
                self.handle_client(connection, address)


def main():
    server = Server(SOCKET_FAMILY, SOCKET_PROTOCOL, ADDRESS)
    server.start()


main()

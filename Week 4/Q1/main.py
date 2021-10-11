import socket

SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM


class PortScanner:
    @staticmethod
    def scan(server, start=1, end=65535):
        print('\nScanning...\n')
        open_port_count = 0
        for port in range(start, end + 1):
            if PortScanner.__connect(server, port):
                print(f'Port {port} is open')
                open_port_count += 1

        if open_port_count == 0:
            print('No ports are available')
        else:
            print(f'\nFound {open_port_count} open port{"s" if open_port_count > 1 else ""}\n')

    @staticmethod
    def __connect(server, port):
        client = socket.socket(SOCKET_FAMILY, SOCKET_PROTOCOL)
        address = (server, port)
        try:
            client.connect(address)
            client.close()
            return True
        except:
            return False


def main():
    server = input('Server: ')
    port_scanner = PortScanner()
    port_scanner.scan(server, 100, 140)


main()

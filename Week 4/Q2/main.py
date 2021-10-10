import socket
import threading

SOCKET_FAMILY = socket.AF_INET
SOCKET_PROTOCOL = socket.SOCK_STREAM
PORT_COUNT = 65535
THREAD_COUNT = 500
PRINT_LOCK = threading.Lock()
UPDATE_PORT_COUNT_LOCK = threading.Lock()


class PortScanner:
    open_port_count = 0

    @staticmethod
    def scan(server, start=1, end=PORT_COUNT):
        for port in range(start, end + 1):
            if PortScanner.__connect(server, port):
                with PRINT_LOCK:
                    print(f'Port {port} is open')

                with UPDATE_PORT_COUNT_LOCK:
                    PortScanner.open_port_count += 1

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

    threads = []

    for i in range(0, THREAD_COUNT + 1):
        start = PORT_COUNT // THREAD_COUNT * i + 1
        end = min([start + PORT_COUNT // THREAD_COUNT - 1, PORT_COUNT])
        scan_thread = threading.Thread(target=port_scanner.scan, args=(server, start, end))
        threads.append(scan_thread)

    print('\nScanning...')

    for i in range(THREAD_COUNT):
        threads[i].start()
        
    for i in range(THREAD_COUNT):
        threads[i].join()

    if PortScanner.open_port_count == 0:
        print('No ports are available')
    else:
        print(f'\nFound {PortScanner.open_port_count} open port{"s" if PortScanner.open_port_count > 1 else ""}\n')


main()

import ssl
import socket
import datetime
import time

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 15000
ADDRESS = (SERVER, PORT)

# Create a server socket 
server = socket.socket()
server.bind(ADDRESS)

# Listen for incoming connections
server.listen()
print(f"Server listening on {SERVER}...")

while(True):
    # Keep accepting connections from clients
    (connection, address) = server.accept()
    
    # Make the socket connection to the clients secure through SSLSocket
    secure_client_socket = ssl.wrap_socket(connection, 
                                        server_side=True, 
                                        ca_certs="./ca.crt", 
                                        certfile="./server.crt",
                                        keyfile="./server.key", 
                                        cert_reqs=ssl.CERT_REQUIRED,
                                        ssl_version=ssl.PROTOCOL_TLSv1_2)

    # Get certificate from the client
    client_cert = secure_client_socket.getpeercert()
    
    clt_subject = dict(item[0] for item in client_cert['subject'])
    clt_commonName = clt_subject['commonName']

    # Check the client certificate bears the expected name as per server's policy
    if not client_cert:
        raise Exception("Unable to get the certificate from the client")
        
    if clt_commonName != 'Anirudh Achal':
        raise Exception("Incorrect common name in client certificate")

    # Check time validity of the client certificate
    t1  = ssl.cert_time_to_seconds(client_cert['notBefore'])
    t2  = ssl.cert_time_to_seconds(client_cert['notAfter'])
    ts  = time.time()

    if ts < t1:
        raise Exception("Client certificate not yet active")
        
    if ts > t2:
        raise Exception("Expired client certificate")

    # Send current server time to the client
    server_time = f'{datetime.datetime.now()}'
    secure_client_socket.send(server_time.encode())
    print(f"Securely sent {server_time} to {address}")

    # Close the connection to the client
    secure_client_socket.close()

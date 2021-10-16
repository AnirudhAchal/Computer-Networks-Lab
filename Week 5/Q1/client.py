
import socket
import ssl
import time

# IP address and the port number of the server
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 15000
SERVER_ADDRESS = (SERVER, PORT)

# Create an SSL context
context = ssl.SSLContext()
context.verify_mode = ssl.CERT_REQUIRED

# Load CA certificate with which the client will validate the server certificate
context.load_verify_locations("./ca.crt")

# Load client certificate
context.load_cert_chain(certfile="./client1.crt", keyfile="./client1.key")

# Create a client socket
clientSocket = socket.socket()

# Make the client socket suitable for secure communication
secureClientSocket = context.wrap_socket(clientSocket)
secureClientSocket.connect(SERVER_ADDRESS)

# Obtain the certificate from the server
server_cert = secureClientSocket.getpeercert()

# Validate whether the Certificate is indeed issued to the server
subject = dict(item[0] for item in server_cert['subject'])
commonName = subject['commonName']

if not server_cert:
    raise Exception("Unable to retrieve server certificate")
    

notAfterTimestamp = ssl.cert_time_to_seconds(server_cert['notAfter'])
notBeforeTimestamp = ssl.cert_time_to_seconds(server_cert['notBefore'])
currentTimeStamp = time.time()

if currentTimeStamp > notAfterTimestamp:
    raise Exception("Expired server certificate")
    
if currentTimeStamp < notBeforeTimestamp:
    raise Exception("Server certificate not yet active")

# Safe to proceed with the communication
msgReceived = secureClientSocket.recv(1024)
print(f"Secure communication received from server: {msgReceived.decode()}")

# Close the sockets
secureClientSocket.close()
clientSocket.close()

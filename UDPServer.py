import socket
import helper as h

# Define some network parameters
TIMEOUT = 20
BUFFER_SIZE = 2048

# set server port number and create a UPD socket
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.settimeout(TIMEOUT)

# binds port number to server's socket s.t. when anyone sends a packet to 
# serverPort, at the IP address of the server, the packet will be directed 
# to this socket
serverSocket.bind(('',serverPort))
print('The server is ready to receive...')

# allows UDPServer to receive and process packets until timeout
while True:
    message, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)   # parameter buffer size
    
    #  handles timeout error
    try:
        clientPort, destPort,segLength,clientCheckSum,message_unpacked = h.unpack(message)
    except socket.timeout:
        print('Server side timeout')
        message_unpacked = 'NACK'.encode()
        
    print(f'INCOMING MESSAGE: \t\t{message_unpacked}\nCLIENT ADDRESS: \t\t{clientAddress}')
    modifiedMessage = str(message_unpacked.decode().upper()) + ' pong!'

    # send back the modified message
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    


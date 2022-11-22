import socket

# set server port number and create a UPD socket
serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# binds port number to server's socket s.t. when anyone sends a packet to 
# serverPort, at the IP address of the server, the packet will be directed 
# to this socket
serverSocket.bind(('',serverPort))
print('The server is ready to receive.')

# allows UDPServer to receive and process packets indefinitely
while True:
    # when packet arrives at the server's socket, it contains a message
    # and the packet's source address (client IP, client port) where we will
    # direct our reply to 
    messsage, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = str(messsage.decode().upper()) + 'pong!'

    # we shall send back the modified message
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    


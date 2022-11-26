'''
TO DO:
-----
[x] deal with timeouts
[x] deal with losses
    [x] artificial losses

'''

import socket
import random

# Define some network parameters
TIMEOUT = 10
BUFFER_SIZE = 2048
LOSS = True
LOSS_RATE = 3

def artificialLoss():
    artificialLoss = random.randint(0,10)
    if artificialLoss<LOSS_RATE:    
        return 1
    return 0

def sendMsg(socket, message,clientAddr, artLoss = LOSS):
    message = message.encode()
    if not artLoss:
        socket.sendto(message, clientAddr)
    else:
        if artificialLoss():
            print('LOSS')
        else:
            socket.sendto(message, clientAddr)
      

def rcvMsg(socket,BUFFER_SIZE = BUFFER_SIZE):
    msg, clientAddress = socket.recvfrom(BUFFER_SIZE)
    msg = msg.decode()
    
    # handles 'loss' caused by client side artificial loss - replicates corrupted data
    if msg == ' ':
        msg = 'NACK'
        print('--')
    else:
        print('Message received')
        msg = str(msg.upper())+ ' PONG!'
    
    # sendMsg(socket, msg, clientAddress)
    return msg, clientAddress
    

if __name__=='__main__':
    # set server port number and create a UPD socket
    serverPort = 12000
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.settimeout(TIMEOUT)
    serverSocket.bind(('',serverPort))
    print('The server is ready to receive...')

    FLAG = True
    while FLAG:
        try:
            msg, clientAddr = rcvMsg(serverSocket)
            sendMsg(serverSocket, msg, clientAddr)
        except socket.timeout:
            print('Server time out...closing connection')
            FLAG = False

    serverSocket.close()


            




import socket
import time
import random
'''
TO DO:
-----
[x] deal with timeouts
[x] deal with losses
    [x] artificial losses
[x] add RTT
'''

# Define some network parameters
TIMEOUT = 2
BUFFER_SIZE = 2048
LOSS = True
LOSS_RATE = 5
WINDOW_SIZE = 3

def sendMsg(socket,message, serverAddr,artLoss=LOSS):
    if artLoss:
        if artificialLoss():
            message = ' '

    print(f'sent {message}')
    socket.sendto(message.encode(), serverAddr)

def rcvMsg(socket, BUFFER_SIZE = BUFFER_SIZE):
    # handles NACK
    serverMsg, serverAddr = socket.recvfrom(BUFFER_SIZE)
    serverMsg = serverMsg.decode()
    return serverMsg, serverAddr
    
def artificialLoss():
    artificialLoss = random.randint(0,10)
    if artificialLoss<LOSS_RATE:    
        return 1
    return 0

def selectiveRepeat(clientSocket,slidingWindow):    
    #  send all messages in window at once
        
    print('to send messgae',slidingWindow)
    while len(slidingWindow)>0:
        serverMsg, serverAddr = rcvMsg(clientSocket)
        print(f'Message receieved: {serverMsg}')
        if serverMsg != 'NACK':
            ack = serverMsg[:-5]
            if ack in slidingWindow:
                idx = slidingWindow.index(ack)
                del slidingWindow[idx]
        for msg in slidingWindow:
            sendMsg(clientSocket, msg, serverAddr)
    

if __name__== "__main__":

    # serverName = '172.20.10.4'     # string containing either IP address of server or hostname of server
    serverName = socket.gethostname()
    serverPort = 12000
    serverAddr = (serverName, serverPort)
    # create client's socket using iPv4 and UDP socet
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.settimeout(TIMEOUT) # set time out 5 sec

    # messages to be sent:
    messages = [str(i)+' ping' for i in range(10)]
    FLAG = len(messages)>0
    timeouts = 0
    while FLAG:
        winSize = WINDOW_SIZE if len(messages)>WINDOW_SIZE else len(messages)
        slidingWindow = messages[:winSize]
        # send all messages in window at once
        for msg in slidingWindow:
            sendMsg(clientSocket, msg, serverAddr)
        try:
            # selectiveRepeat(clientSocket,slidingWindow)
            print('to send messgae',slidingWindow)
            while len(slidingWindow)>0:
                serverMsg, serverAddr = rcvMsg(clientSocket)
                print(f'Message received: {serverMsg}')
                if serverMsg != 'NACK':
                    ack = serverMsg[:-5]
                    if ack in slidingWindow:
                        idx = slidingWindow.index(ack)
                        del slidingWindow[idx]
                        
                for msg in slidingWindow:
                    sendMsg(clientSocket, msg, serverAddr)
            
            del messages[:winSize]
            FLAG = len(messages)>0

        except socket.timeout:
            timeouts +=1
            if timeouts<5:
                print(f'TIMEOUT {timeouts} - remaining msgs in this sliding window {slidingWindow}')
                print('Timeout occurred... retransmitting last message')

            else:
                FLAG = False
                print('Too many timeouts in this connection')

    print('Closing connection...')
    clientSocket.close()
    
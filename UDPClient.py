import socket
import time
import random
import helper as h
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
LOSS_RATE = 4

def sendMsg(socket,message, serverAddr,artLoss=LOSS):
    if artLoss:
        if artificialLoss():
            message = ' '

    # print(f'sent {message}')
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
    RTT = []
    while FLAG:
        RTT.append(time.time())
        sendMsg(clientSocket, messages[0], serverAddr)
        try: 
            serverMsg,serverAddr = rcvMsg(clientSocket)
            # keep retransmitting if the message is NACK
            while serverMsg == 'NACK':
                print('NACK received ... retransmitting last message')
                sendMsg(clientSocket, messages[0], serverAddr)
                serverMsg,serverAddr = rcvMsg(clientSocket)
            
            RTT.append(time.time())
            print(f'Message receieved: {serverMsg} - RTT:{(max(RTT)-min(RTT))*1000} msec')
            
            del messages[0]
            FLAG = len(messages)>0
            RTT = []
            
        
        except socket.timeout:
            RTT.append(time.time())
            timeouts +=1
            if timeouts<10:
                print(f'TIMEOUT {timeouts}')
                print('Timeout occurred... retransmitting last message')
            else:
                FLAG = False
                print('Too many timeouts in this connection')
            

        

    print('Closing connection...')
    clientSocket.close()
    
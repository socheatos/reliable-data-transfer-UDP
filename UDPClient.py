import socket
import time
import random
import helper as h
'''
TO DO:
-----
- do i really want to do go back n?
- handle ACK/NACKs: 
    - if NACK - retransmit
    - if ACK - all good?
- calculate RTT
- make sure timeouts work w multiple message
- artificial loss/bit corruption

LOSS SCENARIOS:
- buffer size too big? - split it up / send separately w sequence number as last word on 
- time outs? - reconnect & retransmit
- no ACK/NACK? - retransmit
'''

# Define some network parameters
TIMEOUT = 5
BUFFER_SIZE = 2048


# serverName = '172.20.10.4'     # string containing either IP address of server or hostname of server
serverName = socket.gethostname()
serverPort = 12000

clientMessage = input('Please enter your message: ')
clientCheckSum = h.checkSum(0, serverPort,clientMessage)
clientSegmentLength = len(clientMessage)+8
clientSegment = h.pack(0,serverPort,clientSegmentLength,clientCheckSum,clientMessage)

# create client's socket using iPv4 and UDP socet
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(TIMEOUT) # set time out 5 sec

clientSocket.sendto(clientSegment, (serverName,serverPort))

# handles timeout error

try:
    serverMsg, serverAddr = clientSocket.recvfrom(BUFFER_SIZE)
    print(f'SERVER MESSAGE: {serverMsg.decode()}')
except socket.timeout:
    print('Client side timeout! Retransmitting...')

clientSocket.close()
import socket
import time
import random
import helper as h
'''
After pinging the server, print the Round Trip Time (RTT)
when the server responds with the corresponding pong.
≈
TO DO:
- packet loss detection
- send retransmission

Notes on Packet Loss
Packets can arrive to find a full queue - but with no place to store such packet, the router will drop that packet i.e. the packe twill be lost.

A packet loss will look like a packet having been transmitted into the network core but never emerging from the network at the destination. The fraction of lost packets increases as traffic intensity increases
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
    print('Client side timeout!')

clientSocket.close()
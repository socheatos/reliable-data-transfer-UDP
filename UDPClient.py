import socket
import time
import random
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

# serverName = '172.20.10.4'     # string containing either IP address of server or hostname of server
serverName = socket.gethostname()
serverPort = 12000

# create client's socket
# AF_INET - underlying network using iPv4
# SOCK_DGRAM - indicates UPD socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.settimeout(1) # set time out 

numIter = int(input('Enter number of packets to send:'))
mssges = [str(i)+' ping ' for i in range(numIter)]
for i in range(numIter):
    artificial_loss_int = random.randint(0,10)
    
    # records the RTT 
    rttStart = time.time()

    # artificial loss 
    if artificial_loss_int < 4:
        print('loss injected')
        continue

    # send message through socket to the destination host 
    # encode() converts string type to byte type
    message = mssges[i]
    clientSocket.sendto(message.encode(), (serverName, serverPort))

    # returns packet arriving from internet at client's socket and packet's source address (server's IP, port number)
    # .recvfrom(x) takes the buffer size x

    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
    rttEnd = time.time()

    if modifiedMessage:
        print(modifiedMessage.decode(), '-',str(rttEnd-rttStart)+'s')
    else:
        print('Request timed out')
    

    # wait for 1 second if nothing received then this packet is marked
    # as loss during transmission

    # print(modifiedMessage.decode(), '-',str(rttEnd-rttStart)+'s')
clientSocket.close()
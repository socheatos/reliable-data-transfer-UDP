'''
Functions taht ensure reliable data transfer. We will be using the ******
protocol to deal with packet loss and retransmission.
 
On the client side:
- availableSeqNum()
- timeout()
- ackReceived()

On the server side:
- 
'''

'''
We will first construct a UDP segment class so it includes the header information and will 
allow for users to attach their application layer messages to the segment. 

We define the segmentcontaining the fields specified below according to [RFC 768]:
- source port (optional): port of sending address, assume to be the prot to which 
a reply should be addressed to in absense of any other information
- destination port: is the internet destination address
- length: length in octets of this user datagram including the header and the data
- checksum

each field is two bytes => 8 bytes + L bytes for data

UDP Field: 
 0      7 8     15 16    23 24    31 
+--------+--------+--------+--------+
|      Source     |    Destination  |
|       Port      |       Port      |
+--------+--------+--------+--------+
|      Length     |     Checksum    |
+--------+--------+--------+--------+
|
|        data octets ...
+--------------- ...


**lets ignore this for now**
The pseudo header is conceptually prefixed to the UDP header containing the source address, destination address, 
protocol, and UDP length. This is used for calculation for the UDP segment and is discarded after, it is not sent.


UDP Pseudo Header (12 Bytes)
 0      7 8     15 16    23 24    31 
+--------+--------+--------+--------+
|           source address          |
+--------+--------+--------+--------+
|        destination address        |
+--------+--------+--------+--------+
|  zero  |protocol|   UDP length    |
+--------+--------+--------+--------+

'''
import struct


def pack(source,destination,length,checksum,msg):
    if isinstance(msg, str):
        msg = msg.encode()
    return struct.pack(f'!4H{len(msg)}s',source,destination,length,checksum,msg)

def unpack(packet):
    msg_size = len(packet)-8
    return struct.unpack(f'!4H{msg_size}s',packet)

def checkSum(source,destination,messages=None,client_side=True):
    source, destination = bin(source), bin(destination)
    data = [source,destination]
    if messages:
        messages = stringToBit(messages)
        data = [source,destination,*messages]
    s = 0
    for i in data:
        i = int(i,2)
        s += i
        s = (s & 0xffff) + (s >> 16) # Take the first 16 bits, and then add 17 bits (the value of the carry is added to the first bit)
    if client_side:
        return (~s & 0xffff)
    return s 

def stringToBit(string):
    '''Converts string to 16-bit signed char and place them in
    a list for checksum calculation'''
    if isinstance(string, bytes):
        string = string.decode()
    res = [format(ord(i),'016b') for i in string]
    return res

# Q: how to handle packet loss?
# Q: how to handle retransmission

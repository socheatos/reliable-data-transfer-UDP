'''
Functions taht ensure reliable data transfer. We will be using the ******
protocol to deal with packet loss and retransmission.
 
On the client side:
- availableSeqNum()
- timeout()
- ackReceived()


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
    # https://www.zhihu.com/question/47025566/answer/103966103
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

# Reliable Data Transfer over UDP

The objective of this assignment is to build a reliable data transfer *application* based on a UPD protocol.

For each message that the client sends, it should print out the Round Trip Time (RTT),i.e. the delay between client sending the message and receiving it.

## Table of Contents:
1. [UPD segment structure](#udp-segment-structure)
2. [Reliable Data Transfer Protocol](#reliable-data-transfer-protocols)
---
## UDP segment structure

We define the segment containing the fields specified below according to [[RFC 768]](https://www.rfc-editor.org/rfc/rfc768):
- Source port (optional): port of sending address, assume to be the prot to which 
a reply should be addressed to in absense of any other information
- Destination port: is the internet destination address
- Length: length in octets of this user datagram including the header and the data
- Checksum:  16-bit one's complement of the one's complement sum of a
pseudo header of information from the IP header, the UDP header, and the
data,  padded  with zero octets  at the end (if  necessary)  to  make  a
multiple of two octets.
```
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
```
Although a pseudo header is defined in the document, we will ignore that for now and focus solely on the segment for simplicity.
## Reliable Data Transfer protocols
UPD is an unreliable protocol, this means that a packet sent either by the client or server might be lost or corrupted. So we want to design mechanisms that would detect packet loss, retransmissions, and account for this delay in the total RTT printed out on the client side.These mechanisms will be implemented using the **Go-Back-N**  protocol


# Reliable Data Transfer over UDP

The objective of this assignment is to build a reliable data transfer *application* based on a UPD protocol.

For each message that the client sends, it should print out the Round Trip Time (RTT),i.e. the delay between client sending the message and receiving it.

## UDP segment structure

## Reliable Data Transfer protocols
UPD is an unreliable protocol, this means that a packet sent either by the client or server might be lost or corrupted. So we want to design mechanisms that would detect packet loss, retransmissions, and account for this delay in the total RTT printed out on the client side. We will implement all these mechanisms using the **Go-Back-N**  protocol

## Go-Back-N

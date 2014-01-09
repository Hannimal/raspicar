#!/usr/bin/python

import smbus
import time
bus = smbus.SMBus(1)
address = 0x2a

sendstring = "Hello!"
bytearraytowrite = map(ord, sendstring)

def toWrite(a):
    for i in a:
		bus.write_byte(address, i)


while True:
    sdata = "" 
    rdata = ""
    for i in range(0, 5):
            rdata += chr(bus.read_byte(address));
    print rdata
    print bytearraytowrite
    print "".join(map(chr, bytearraytowrite)) #Will convert bytearray to string.
    toWrite(bytearraytowrite)
    time.sleep(1)
    #time.sleep(.04);
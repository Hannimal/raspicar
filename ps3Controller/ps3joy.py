#!/usr/bin/env python
# coding: Latin-1

import sys
import smbus
import time
bus = smbus.SMBus(1)
address = 0x2a

try:
    pipe = open('/dev/input/js0', 'r')
    print('/dev/input/js0 Available')
except:
    print('/dev/input/js0 not Available')
    sys.exit(0)
msg = []
position = [0,0,0,0]

def StringToBytes(val):
    retVal = []
    for c in val:
            retVal.append(ord(c))
    return retVal

def sendData(val):
    try:
        #print(val)
        bus.write_i2c_block_data(address, 1, val)
    except:
        pass

def getRange(device):
    status = bus.read_byte(device)
    #time.sleep(0.01)        
    return status

while 1:
    try:
        for char in pipe.read(1):
            msg += [char]
	    #print(msg)
        if len(msg) == 8:
                # Button event if 6th byte is 1
                if ord(msg[6]) == 1:
                    position[3] = ord(msg[7])
                    position[2] = ord(msg[4])
                    print(getRange(address))
                # Axis event if 6th byte is 2
                if ord(msg[6]) == 2: # define Axis
                    if ord(msg[7]) == 2: # define right joy
                        position[0] = ord(msg[5])
                    if ord(msg[7]) == 1: # define left joy
                        position[1] = ord(msg[5])
                sendData(position)
                msg = []
    except KeyboardInterrupt:
        sendData([0,0])
        raise
    except:
        print ('Lost Connection')
        sendData([0,0])
        sys.exit(0)
        

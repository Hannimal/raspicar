#!/usr/bin/env python
# coding: Latin-1

import sys
import smbus
import time
from array import array

bus = smbus.SMBus(1)
address = 0x2a
battery = 0x0b

msg = [0, 0, 0, 0, 0, 0, 0]

def sendData(val):
    try:
        #print(val)
        bus.write_i2c_block_data(address, 1, val)
    except:
        pass
    
def readWord(address,cmd):
        word = []
        try:
                nul = bus.read_byte_data(address,0)
                word = bus.read_word_data(address,cmd)
                return word
        except:
                pass

voltage = readWord(battery,0x09)*0.001
#print voltage
msg[2] = ord("a")
msg[3] = ord("b")
msg[4] = ord("c")
msg[5] = ord("d")

while 1:
    print(msg)
    sendData(msg)
    time.sleep(1)
    
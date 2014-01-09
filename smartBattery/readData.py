#!/usr/bin/python

import time
from smbus import SMBus
from array import array

address = 0x0b
read = bytearray()
bus = SMBus(1) # 1 indicates /dev/i2c-1

def readBlock(address,cmd):
    msg = []
    try:
        nul = bus.read_byte_data(address,0)
        read = bus.read_i2c_block_data(address,cmd)
        count = read[0] + 1
        for i in range(1,count):
            msg += [str(unichr(read[i]))]
        value = array('B', map(ord,msg)).tostring()
    except:
        pass
    return value

def readWord(address,cmd):
        msg = []
        try:
                nul = bus.read_byte_data(address,0)
                msg = bus.read_word_data(address,cmd)
        except:
                pass
        return msg

print("Manufacturer",readBlock(address,0x20))
print("Device Name",readBlock(address,0x21))
print("Device Chemistry",readBlock(address,0x22))
Celsius = ((readWord(address,0x08))*0.1) - 273.15
print("Temperature","%.2f" % Celsius)
print("Voltage",readWord(address,0x09)*0.001)
print("Current",readWord(address,0x0a)*0.001)
print("Charge",readWord(address,0x0d))
print("Time",readWord(address,0x11))

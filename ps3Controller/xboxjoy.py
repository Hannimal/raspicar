#!/usr/bin/env python
# coding: Latin-1

# Appendix: Xbox 360 Controller Keys
# --------------
# X1 Y1 X2 Y2
# du dd dl dr
# back guide start
# TL TR
# A B X Y
# LB RB LT RT

import sys
import smbus
import time
from lib import xbox_read
from array import array

bus = smbus.SMBus(1)
address = 0x2a

rt_intensity = 0
lt_intensity = 0
y1_intensity = 0
x2_intensity = 0
msgcount = 0
msg = [0,0,0,0,0]

def sendData(val):
    try:
        #print(val)
        bus.write_i2c_block_data(address, 1, val)
    except:
        pass

def ProcessValue(value):
    value = value / 255
    #if (value < 0):
    #    value = 255 - abs(value)
    if (value >= 127):
        value = 127
    if (value <= -127):
        value = 129
    #print(value)
    return value

def ProcessTriggers():
    trigger = ((rt_intensity/2) - (lt_intensity/2)) * -1
    if (trigger > -30 and trigger < 30):
        trigger = 0
    #print trigger
    return trigger

def ProcessButtons(key , value):
    if  key == 'A':
        msg[2]=1
        msg[3]=value
    elif key == 'B':
        msg[2]=2
        msg[3]=value
    elif key == 'X':
        msg[2]=3
        msg[3]=value
    elif key == 'Y':
        msg[2]=4
        msg[3]=value
    #print (key , ' ' , value)
    return 0

try:
    for event in xbox_read.event_stream(deadzone=12000):
        if   (event.key == 'LT'):
            lt_intensity = event.value
        elif (event.key == 'RT'):
            rt_intensity = event.value
        elif (event.key == 'Y1'):
            y1_intensity = event.value
        elif (event.key == 'X2'):
            x2_intensity = event.value
        else:
            ProcessButtons(event.key , event.value)
        msg[0] = ProcessValue(x2_intensity)
        msg[1] = ProcessValue(y1_intensity) #msg[1] = ProcessTriggers()
        msg[4] +=1
        sendData(msg)
        if msg[4] > 1000:
            msg[4] = 0
except:
    print ('Lost Connection')
    sendData([0,0,0,0,0])
    sys.exit(0)
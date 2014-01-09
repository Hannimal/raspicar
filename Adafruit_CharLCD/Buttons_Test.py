#!/usr/bin/env python
 
from time import sleep
import os
import RPi.GPIO as GPIO

#Assign Buttons to Pins

button1 = 9
button2 = 4
button3 = 23
button4 = 10

GPIO.setmode(GPIO.BCM)

GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
while True:
        try:  
            GPIO.wait_for_edge(button1, GPIO.FALLING)  
            print "button1"
            GPIO.wait_for_edge(button2, GPIO.FALLING)  
            print "button2"
            GPIO.wait_for_edge(button3, GPIO.FALLING)  
            print "button3"
            GPIO.wait_for_edge(button4, GPIO.FALLING)  
            print "button4"
        except KeyboardInterrupt: 
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
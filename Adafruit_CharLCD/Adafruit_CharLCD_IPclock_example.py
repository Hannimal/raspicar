#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

import RPi.GPIO as GPIO

#Assign Buttons to Pins

#Assign Pins to Buttons
BUTTON_1_PIN    = 9
BUTTON_2_PIN    = 4
BUTTON_3_PIN    = 23
BUTTON_4_PIN    = 10

GPIO.setmode(GPIO.BCM)

#configure GPIO For input Buttons
GPIO.setup(BUTTON_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_3_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_4_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lcd = Adafruit_CharLCD()

lancmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
wlancmd ="ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
bitratecmd = "iwconfig wlan0 | grep Rate: | awk '{print $1 $2 $3}'"
linkqcmd = "iwconfig wlan0 | grep Link | awk '{print $2}'"
memcmd = "cat /proc/meminfo | grep MemFree | awk '{print $2$3}'"
cpucmd = "cat /proc/cpuinfo | grep BogoMIPS | awk '{print $3}'"
tempcmd = "/opt/vc/bin/vcgencmd measure_temp | cut -c6-11"

lcd.begin(16,2)

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output
        
def my_callback_1(BUTTON_1_PIN):
    if wlan!='':
        lcd.clear()
        lcd.message('Wlan0 IP:  \n')
        lcd.message('  %s\n' %(wlan) )
        sleep(2)
        lcd.clear()
        lcd.message('%s\n' %(bitrateinfo) )
        lcd.message('%s\n' %(linkqinfo) )
        sleep(2)
    if lan!='':
        lcd.clear()
        lcd.message('Eth0 IP:  \n')
        lcd.message('  %s\n' %(lan) )
        sleep(2)

def my_callback_2(BUTTON_1_PIN):
    lcd.clear()
    lcd.message('CPU Temperature: \n')
    lcd.message('          %s'  % (tempinfo) )
    sleep(2)

def my_callback_3(BUTTON_1_PIN):
    lcd.clear()
    lcd.message('Free Memory: \n')
    lcd.message('         %s'  % (meminfo) )
    sleep(2)
    
def my_callback_4(BUTTON_1_PIN):
    lcd.clear()
    lcd.message('CPU Frequency: \n')
    lcd.message('       %s'  % (cpuinfo) )
    sleep(2)

GPIO.add_event_detect(BUTTON_1_PIN, GPIO.RISING, callback=my_callback_1)
GPIO.add_event_detect(BUTTON_2_PIN, GPIO.RISING, callback=my_callback_2)
GPIO.add_event_detect(BUTTON_3_PIN, GPIO.RISING, callback=my_callback_3)
GPIO.add_event_detect(BUTTON_4_PIN, GPIO.RISING, callback=my_callback_4)


while 1:
    try:
        lan = run_cmd(lancmd)
        wlan = run_cmd(wlancmd)
        bitrateinfo = run_cmd(bitratecmd)
        linkqinfo = run_cmd(linkqcmd)
        meminfo = run_cmd(memcmd)
        cpufreq = run_cmd(cpucmd)
        cpuinfo = cpufreq[:-1]+ 'Mhz'
        tempinfo = run_cmd(tempcmd)
        '''
        if wlan!='':
            lcd.clear()
            lcd.message('Wlan0 IP:  \n')
            lcd.message('  %s\n' %(wlan) )
            sleep(2)
            lcd.clear()
            lcd.message('%s\n' %(bitrateinfo) )
            lcd.message('%s\n' %(linkqinfo) )
            sleep(2)
        if lan!='':
            lcd.clear()
            lcd.message('Eth0 IP:  \n')
            lcd.message('  %s\n' %(lan) )
            sleep(2)
        lcd.clear()
        lcd.message('Free Memory: \n')
        lcd.message('         %s'  % (meminfo) )
        sleep(2)
        lcd.clear()
        lcd.message('CPU Frequency: \n')
        lcd.message('       %s'  % (cpuinfo) )
        sleep(2)
        lcd.clear()
        lcd.message('CPU Temperature: \n')
        lcd.message('          %s'  % (tempinfo) )
        sleep(2)
        '''
        lcd.clear()
        lcd.message(datetime.now().strftime('   %d %m %Y\n    %H:%M:%S\n'))
        sleep(5)
        '''
        lcd.clear()
        lcd.message('  Raspberry Pi\n')
        lcd.message('Helder Barreiros\n')
        sleep(2)
        '''
    except KeyboardInterrupt:
        lcd.clear()
        lcd.message('    Bye Bye...\n')
        sleep(3)  
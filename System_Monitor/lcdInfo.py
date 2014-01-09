#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
from CharLCDLib import CharLCDLib
from subprocess import *
from time import sleep, strftime
from datetime import datetime
from smbus import SMBus
from array import array

lcd = CharLCDLib()
address = 0x0b
read = bytearray()
bus = SMBus(1)

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

lancmd =  "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
wlancmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
bitratecmd = "iwconfig wlan0 | grep Rate: | awk '{print $1 $2 $3}'"
linkqcmd = "iwconfig wlan0 | grep Link | awk '{print $2}'"
memcmd = "cat /proc/meminfo | grep MemFree | awk '{print $2$3}'"
cpucmd = "cat /proc/cpuinfo | grep BogoMIPS | awk '{print $3}'"
tempcmd = "/opt/vc/bin/vcgencmd measure_temp | cut -c6-11"
cpusagecmd = "mpstat | grep all | awk '{print $11}'"

def readBlock(address,cmd):
    msg = []
    try:
        read = bus.read_byte_data(address,0)
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
                msg = bus.read_byte_data(address,0)
                msg = bus.read_word_data(address,cmd)
        except:
                pass
        return msg
        
def getBatteryTemp():
    temp = 'not connected'
    try:
        Celsius = ((readWord(address,0x08))*0.1) - 273.15
        temp = str(Celsius) + 'C'
    except:
        pass
    return temp
    
def getBatteryCharge():
    value = 'not connected'
    try:
        charge = readWord(address,0x0d)
        value = str(charge) + '%'
    except:
        pass
    return value

def getBatteryTime():
    value = 'not connected'
    try:
        time = readWord(address,0x11)
        value = str(time) + ' min'
    except:
        pass
    return value
    
def getBatteryVoltage():
    value = 'not connected'
    try:
        voltage = readWord(address,0x09)
        value = 'V=' + str(voltage*0.001) + 'v'
    except:
        pass
    return value

def getBatteryCurrent():
    value = 'not connected'
    try:
        current = readWord(address,0x0a)
        value = 'I=' + str(current*0.001) + 'ma'
    except:
        pass
    return value

def Quitcallback(button1):
    lcd.clear()
    lcd.message('Bye Bye...',2)
    sleep(3)
    lcd.noDisplay()
    sys.exit()
    
def startStopCarCallback(button4):
    lcd.clear()
    lcd.message('Start Carserver...',2)
    run_cmd("/etc/init.d/carserver stop")
    run_cmd("/etc/init.d/carserver start")
    
def startStopPs3JoyCallback(button4):
    lcd.clear()
    lcd.message('Starting xboxJoy',1)
    #run_cmd("/etc/init.d/xboxjoy stop")
    #run_cmd("/etc/init.d/xboxjoy start")
    run_cmd("python /home/pi/rccar/ps3Controller/xboxjoy.py")
    sleep(2)
    

lcd.begin(16,2)
GPIO.add_event_detect(button1, GPIO.RISING, callback=Quitcallback)
GPIO.add_event_detect(button3, GPIO.RISING, callback=startStopPs3JoyCallback)
GPIO.add_event_detect(button4, GPIO.RISING, callback=startStopCarCallback)

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

while 1:
    try:
        cpufreq = run_cmd(cpucmd)
        cpuinfo = cpufreq[:-1]+ 'Mhz'
        cpuUsageInfo = str(100-float(run_cmd(cpusagecmd).rstrip())) + '%'

        
        if run_cmd(wlancmd)!='':
            lcd.clear()
            lcd.message('Wlan0 IP',1 )
            lcd.message("\n",0)
            lcd.message(run_cmd(wlancmd), 3 )
            sleep(2)
            lcd.clear()
            lcd.message(run_cmd(bitratecmd), 1 )
            lcd.message("\n",0)
            lcd.message(run_cmd(linkqcmd), 3 )
            sleep(2)
        if run_cmd(lancmd)!='':
            lcd.clear()
            lcd.message('Eth0 IP:', 1)
            lcd.message("\n",0)
            lcd.message(run_cmd(lancmd), 3 )
            sleep(2)
        lcd.clear()
        lcd.message('Free Memory: \n', 1)
        lcd.message(run_cmd(memcmd), 3 )
        sleep(2)
        lcd.clear()
        lcd.message('CPU Frequency: \n', 1)
        lcd.message('%s'  % (cpuinfo), 3 )
        sleep(2)
        lcd.clear()
        lcd.message('CPU Utilization: \n',1)
        lcd.message('%s'  % (cpuUsageInfo),3 )
        sleep(2)
        lcd.clear()
        lcd.message('CPU Temperature: \n', 1)
        lcd.message(run_cmd(tempcmd).strip(), 3 )
        sleep(2)
        lcd.clear()
        lcd.message('Battery Temp: \n', 1)
        lcd.message(getBatteryTemp().strip(), 3 )
        sleep(2)
        lcd.clear()
        stringH = 'Battery Info: \n'
        stringL = getBatteryCharge() + '(' + getBatteryTime() + ')'
        lcd.message(stringH, 1)
        lcd.message(stringL, 1)
        sleep(2)
        lcd.clear()
        stringH = getBatteryVoltage() + '\n'
        stringL = getBatteryCurrent().rstrip() + '\n'
        lcd.message(stringH, 2)
        lcd.message(stringL, 2)
        sleep(2)
        lcd.clear()
        lcd.message(datetime.now().strftime('%d-%m-%Y'),2)
        lcd.message("\n",0)
        lcd.message(datetime.now().strftime('%H:%M:%S'),2)
        sleep(2)
        lcd.clear()
        lcd.message('Raspberry Pi',2)
        lcd.message("\n",0)
        lcd.message('Helder Barreiros  ',1)
        sleep(2)
    except KeyboardInterrupt:
        lcd.clear()
        lcd.message('Bye Bye...',2)
        sleep(3)
        lcd.noDisplay()
        break
    

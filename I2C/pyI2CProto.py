import smbus
import time

LCD_ADDR = 0x2a

def StringToBytes(val):
        retVal = []
        for c in val:
                retVal.append(ord(c))
        return retVal

def SayHello():
    try:
        bus = smbus.SMBus(1)
        messageInBytes = StringToBytes("Isto e uma mensagem maior")
        bus.write_i2c_block_data(LCD_ADDR, 1, messageInBytes)
    except Exception: 
        pass
    
if __name__ == "__main__":
        while True:
                SayHello()
                time.sleep(0.2)
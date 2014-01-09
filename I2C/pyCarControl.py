#import serial;
import pygame;
import os;
from pygame.locals import *;
import smbus
import time
bus = smbus.SMBus(1)
address = 0x2a

os.environ["SDL_VIDEODRIVER"] = "dummy"

def toWrite(a):
    for i in a:
    	bus.write_byte(address, i)


def clear_screen():
    os.system('clear')

def getOrder(run):
        for event in pygame.event.get():
            if (event.type == KEYDOWN):
                keyinput = pygame.key.get_pressed();

                #complex orders
                if keyinput[pygame.K_UP] and keyinput[pygame.K_RIGHT]:
                    run[1] = 21;
                elif keyinput[pygame.K_UP] and keyinput[pygame.K_LEFT]:
                    run[1] = 22;
                elif keyinput[pygame.K_DOWN] and keyinput[pygame.K_RIGHT]:
                    run[1] = 23;
                elif keyinput[pygame.K_DOWN] and keyinput[pygame.K_LEFT]:
                    run[1] = 24;

                #simple orders
                elif keyinput[pygame.K_UP]:
                    run[1] = 11;
                elif keyinput[pygame.K_DOWN]:
                    run[1] = 12;
                elif keyinput[pygame.K_RIGHT]:
                    run[1] = 13;
                elif keyinput[pygame.K_LEFT]:
                    run[1] = 14;
                
                elif keyinput[pygame.K_1]:
                	run[1] = 1;
                elif keyinput[pygame.K_2]:
                	run[1] = 2;
                elif keyinput[pygame.K_3]:
                	run[1] = 3;

                #exit
                elif keyinput[pygame.K_x] or keyinput[pygame.K_q]:
                    print 'exit';
                    run[0] = False;
                    run[1] = 0;
                    
            elif event.type == pygame.KEYUP:

                #single key
                if (run[1] < 20):
                    run[1] = 0;

                #up-right
                elif (run[1] == 21):
                    if event.key == pygame.K_RIGHT:
                        run[1] = 11;
                    elif event.key == pygame.K_UP:
                        run[1] = 13;

                #up-left
                elif (run[1] == 22):
                    if event.key == pygame.K_LEFT:
                        run[1] = 11;
                    elif event.key == pygame.K_UP:
                        run[1] = 14;

                #back-right
                elif (run[1] == 23):
                    if event.key == pygame.K_RIGHT:
                        run[1] = 12;
                    elif event.key == pygame.K_DOWN:
                        run[1] = 13;

                #back-left
                elif (run[1] == 24):
                    if event.key == pygame.K_LEFT:
                        run[1] = 12;
                    elif event.key == pygame.K_DOWN:
                        run[1] = 14;
                    
        return run;
            
def main():
    
    clear_screen()
    
    print '\nStarting CarControl v.0.3\n';

    #ser = serial.Serial('/dev/tty.usbmodem411', 115200, timeout=1);
    
    pygame.init();
    run = [True,0];
    previous = -1

    while run[0]:
        run = getOrder(run);
        
        #debug
        print 'current orders: ' + str(run[1]);
        
        if (run[1] != previous):
            previous = run[1];
            bytearraytowrite = map(ord, str(run[1] + 65))

            toWrite(bytearraytowrite);
            #ser.write(chr(run[1] + 65));
            print run[1];

    ser.close();
    
    exit('\nGoodbye!\n')

if __name__ == "__main__":
	main()
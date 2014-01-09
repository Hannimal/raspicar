#!/usr/bin/python

import pygame;
import os;
from pygame.locals import *;
import smbus
import time
bus = smbus.SMBus(1)
address = 0x2a

class pyscope :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
    
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
                if (keyinput[pygame.K_UP] or keyinput[pygame.K_q]) and (keyinput[pygame.K_RIGHT] or keyinput[pygame.K_p]):
                    run[1] = 89;
                elif (keyinput[pygame.K_UP] or keyinput[pygame.K_q]) and (keyinput[pygame.K_LEFT] or keyinput[pygame.K_o]):
                    run[1] = 78;
                elif (keyinput[pygame.K_DOWN] or keyinput[pygame.K_a]) and (keyinput[pygame.K_RIGHT] or keyinput[pygame.K_p]):
                    run[1] = 23;
                elif (keyinput[pygame.K_DOWN] or keyinput[pygame.K_a]) and (keyinput[pygame.K_LEFT] or keyinput[pygame.K_o]):
                    run[1] = 12;

                #simple orders
                elif keyinput[pygame.K_UP] or keyinput[pygame.K_q]:
                    run[1] = 8;
                elif keyinput[pygame.K_DOWN] or keyinput[pygame.K_a]:
                    run[1] = 2;
                elif keyinput[pygame.K_RIGHT] or keyinput[pygame.K_p]:
                    run[1] = 6;
                elif keyinput[pygame.K_LEFT] or keyinput[pygame.K_o]:
                    run[1] = 4;
                
                elif keyinput[pygame.K_1]:
                	run[1] = 50;
                elif keyinput[pygame.K_2]:
                	run[1] = 60;
                elif keyinput[pygame.K_3]:
                	run[1] = 70;

                #exit
                elif keyinput[pygame.K_ESCAPE]:
                    print 'exit';
                    run[0] = False;
                    run[1] = 0;
                    
            elif event.type == pygame.KEYUP:

                #single key
                if (run[1] < 10):
                    run[1] = 0;

                #up-right
                elif (run[1] == 89 ):
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_p):
                        run[1] = 9 ;
                    elif (event.key == pygame.K_UP or event.key == pygame.K_q):
                        run[1] = 6;

                #up-left
                elif (run[1] == 78):
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_o):
                        run[1] = 8;
                    elif (event.key == pygame.K_UP or event.key == pygame.K_q):
                        run[1] = 4;

                #back-right
                elif (run[1] == 23):
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_p):
                        run[1] = 2;
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_a):
                        run[1] = 6;

                #back-left
                elif (run[1] == 12):
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_o):
                        run[1] = 2;
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_a):
                        run[1] = 4;
                    
        return run;
            
def main():
    scope = pyscope()
    pygame.init();
    run = [True,0];
    previous = -1

    while run[0]:
        run = getOrder(run);
        
        #debug
        #print 'current orders: ' + str(run[1]);
        
        if (run[1] != previous):
            previous = run[1];
            bytearraytowrite = map(ord, str(run[1]))
            toWrite(bytearraytowrite);
            print run[1];
    
    exit('\nGoodbye!\n')

if __name__ == "__main__":
	main()

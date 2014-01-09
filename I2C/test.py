#!/usr/bin/python

import curses
import smbus
bus = smbus.SMBus(1)
address = 0x2a

#init the curses screen
stdscr = curses.initscr()
curses.cbreak()
curses.noecho()
stdscr.keypad(1)

print "press q to quit"
quit=False
# loop
while quit !=True:
    try:
        c = stdscr.getch()
        stdscr.addstr(0,0,curses.keyname(c))
        if curses.keyname(c) == "q" :
            quit=True
        elif curses.keyname(c) == "a":
            bus.write_byte(address, c)
        else: bus.write_byte(address,ord("s"))
        time.sleep(1)
        bus.write_byte(address,ord("s"))
    except IOError: pass
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
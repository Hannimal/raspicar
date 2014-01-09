#!/usr/bin/python27
 
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
import json
import time
import multiprocessing
#import serialProcess
 
define("port", default=8080, help="run on the given port", type=int)
 
clients = []

lcd = Adafruit_CharLCD()

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('gamepad.html')
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        clients.append(self)
        self.write_message("connected")
 
    def on_message(self, message):
        message = message.encode('utf-8')
        print message
        self.write_message('got it!')
        lcd.clear()
        lcd.message(message)
        for i in range(1-16):
            lcd.scrollDisplayLeft()
            print(i)
            sleep(.5)
        #q = self.application.settings.get('queue')
        #q.put(message)
 
    def on_close(self):
        print 'connection closed'
        clients.remove(self)
 
################################ MAIN ################################
 
def main():
 
    taskQ = multiprocessing.Queue()
    resultQ = multiprocessing.Queue()
 
    #sp = serialProcess.SerialProcess(taskQ, resultQ)
    #sp.daemon = True
    #sp.start()
 
    # wait a second before sending first task
    time.sleep(1)
    taskQ.put("first task")
 
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler)
        ], queue=taskQ
    )
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port,address="0.0.0.0")
    print "Listening on port:", options.port
    #tornado.ioloop.IOLoop.instance().start()
 
    def checkResults():
        if not resultQ.empty():
            result = resultQ.get()
            print "tornado received from arduino: " + result
            for c in clients:
                c.write_message(result)
 
    mainLoop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(checkResults, 10, io_loop = mainLoop)
    scheduler.start()
    mainLoop.start()
 
if __name__ == "__main__":
    main()
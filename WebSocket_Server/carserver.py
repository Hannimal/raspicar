#!/usr/bin/python27
 
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.gen
from tornado.options import define, options
from time import sleep
import time
import multiprocessing
import smbus
bus = smbus.SMBus(1)
address = 0x2a
 
define("port", default=8080, help="run on the given port", type=int)
 
clients = []

def StringToBytes(val):
        retVal = []
        for c in val:
                retVal.append(ord(c))
        return retVal

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
        #print message
        message = message + '>'
        try:
            bus = smbus.SMBus(1)
            messageInBytes = StringToBytes(message)
            bus.write_i2c_block_data(address, 1, messageInBytes)
        except Exception: 
            pass
        
 
    def on_close(self):
        print 'connection closed'
        clients.remove(self)
 
################################ MAIN ################################
 
def main():
 
    taskQ = multiprocessing.Queue()
    #resultQ = multiprocessing.Queue()
 
    #sp = serialProcess.SerialProcess(taskQ, resultQ)
    #sp.daemon = True
    #sp.start()
 
    # wait a second before sending first task
    #time.sleep(1)
    #taskQ.put("first task")
 
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
 
    #def checkResults():
    #    if not resultQ.empty():
    #        result = resultQ.get()
    #        print "tornado received from arduino: " + result
    #        for c in clients:
    #            c.write_message(result)
 
    mainLoop = tornado.ioloop.IOLoop.instance()
    #scheduler = tornado.ioloop.PeriodicCallback(checkResults, 10, io_loop = mainLoop)
    #scheduler.start()
    mainLoop.start()
 
if __name__ == "__main__":
    main()
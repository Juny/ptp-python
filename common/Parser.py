'''
Created on 2012-9-23

@author: jun
'''
import threading
import thread

class Parser(object):
    
    onMessageReceive = None
    buffer = ""
    conditionLock = threading.Condition()
    waiting = True
    
    def __init__(self):
        thread.start_new_thread(self.tryToParse,())
    
    def parse(self, data):
        self.conditionLock.acquire()
        self.buffer = "%s%s"%(self.buffer,data)
        if self.waiting:
            self.conditionLock.notify()
        self.conditionLock.release()
    
    def tryToParse(self):
        while 1:
            print 'in tryToParse.'
            self.conditionLock.acquire()
            index = self.buffer.find("\n")
            if index == -1:
                self.waiting = True
                self.conditionLock.wait()
                self.isParsing = False
                self.conditionLock.release()
                continue                
            line = self.buffer[0:index]
            self.buffer = self.buffer[index+1:len(self.buffer)]
            self.conditionLock.release()
            self.onMessageReceive(line)
    
class CmdParser(Parser):
    pass

class TransDataParser(Parser):
    pass


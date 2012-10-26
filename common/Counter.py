'''
@author: jun
'''

import time
import thread

import traceback
import sys
    
class Counter(object):
    
    counterDict = None
    dictLock = thread.allocate_lock()
    
    def __init__(self):
        self.counterDict = {}
    
    def increase(self,key):
        self.dictLock.acquire()
        self.counterDict[key] = self.counterDict.get(key,0) + 1 
        self.dictLock.release()       
    
    def decrease(self,key):
        self.dictLock.acquire()
        self.counterDict[key] = self.counterDict.get(key,0) - 1 
        self.dictLock.release()       

"""
每秒清空一次数据，并调用callback
"""
class PerSecondCounter(Counter):
    
    callback = None
    
    def __init__(self, callbackM):
        Counter.__init__(self)
        self.callback = callbackM
        thread.start_new_thread(self.check, ())   
    
    def check(self):
        while 1:
            self.dictLock.acquire()
            tmpdict = self.counterDict
            self.counterDict = {}
            self.dictLock.release()
            if len(tmpdict) > 0 and self.callback != None:
                self.callback(tmpdict)
            time.sleep(1)
            

if __name__ == '__main__':
    def logCounter(counters):
        print 'logCounter : ',counters
    
    def test(counter):
        while 1:
            counter.decrease('test')
            counter.increase('test')
            time.sleep(0.1)
        
    try:
        counter = PerSecondCounter(logCounter)
        while 1:
            counter.increase('test')
            counter.decrease('test')
            counter.increase('test')
        input("wait...")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    
    
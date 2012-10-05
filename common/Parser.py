'''
Created on 2012-9-23

@author: jun
'''
import string

class Parser(object):
    
    #MessageReceiveHandler
    onMessageReceive = None
    
    def parse(self):
        pass
    
class CmdParser(Parser):
    def parse(self, data):
        print 'in parser.%s' % data
        for s in string.split(data,'###'):
            if s == '':
                continue
            self.onMessageReceive(s)

class TransDataParser(Parser):
    pass


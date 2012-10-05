'''
Created on 2012-9-21

@author: jun
'''

import socket
import string
import sys

class Server(object):
    
    def msgReceiveHandler(self,msg):
        pass
    
    def setParser(self,parser):
        self.parser = parser
        self.parser.onMessageReceive = self.msgReceiveHandler
    
    def start(self,port):
        '''
        Constructor
        '''
        myHost = ''
        myPort = port
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        serverSocket.bind((myHost, myPort)) 
        serverSocket.listen(5) 
        
        print 'start complete.'
    
        try:
            while True:
                #connection == socket
                connection, address = serverSocket.accept() 
                print('Server connected by', address) 
                while True:
                    data = connection.recv(256)
                    if not data:
                        print('no data.')
                        break 
                    print('recv=>' + data)
                    self.parser.parse(data) 
                    connection.send('ok.')
                connection.close()
        except Exception:
            #connection.send('error.' + 'Exception..' + e)
            connection.close()
            import traceback
            traceback.print_exc(file=sys.stdout)

class AgentServer(Server):
    
    def setMaster(self,master):
        self.master = master
        
    def msgReceiveHandler(self,msg):
        cmd = string.split(msg,'##')
        if len(cmd) > 1:
            self.master.execute(cmd[0],string.split(cmd[1],'#'))
        else:
            self.master.execute(cmd[0])
            



class ControlServer(Server):
    pass


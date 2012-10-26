'''
@author: jun
'''

import socket
import string
import sys
#import time
import re
from common import Counter
from common import Sqlite

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
                    data = connection.recv(512)
                    if not data:
                        print('no data.')
                        break 
                    print('recv=>' + data)
                    self.parser.parse(data) 
                    connection.send('ok.')
                connection.close()
        except Exception:
            print 'Server Stop.'
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
    
    tpsCounter = None
    db = None
    
    def __init__(self, db_path):
        self.db = Sqlite.DbPorxy.getInstance(db_path)
        self.tpsCounter = Counter.PerSecondCounter(self.tpsCallback)
            
    def tpsCallback(self,counter_dict):
        sqlList = []
        for key in counter_dict.keys():
            sqlList.append("insert into TranPerSecond values(%s,'%s',%s)"%("strftime('%s','now')",key,counter_dict.get(key)))
        self.db.executeSqlBatch(sqlList)

    """
    "{'Type':'Transaction','Time':0,'Value':[{'Test1':0.2,'status':0},{'Test2':0.5,'status':0}]}"
    """
    def msgReceiveHandler(self, msg):
        pattern = re.compile(r"{'Type':'(.*?)','Time':(.*?),'Value':[[](.*)]}")
        match = pattern.match(msg)
        #type,time,value:match.group(1),match.group(2),match.group(3)
        msgType = match.group(1)
        #msgTime = match.group(2)
        msgValues = match.group(3)
        sqlList = []
        if msgType == 'Transaction':
            p = re.compile(r"{'(.*?)':(.*?),'(.*?)':(.*?)}")
            for value in p.findall(msgValues):
                self.tpsCounter.increase(value[0])
                sqlList.append("insert into Trans(Time, TranName, Duration, Status) values(%s,'%s',%s,%s)"%("strftime('%s','now')", value[0], value[1], value[3]))
        self.db.executeSqlBatch(sqlList)
        


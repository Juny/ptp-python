'''
Created on 2012-9-23

@author: jun
'''
import subprocess
import sys
import os
import platform

class Master(object):
    '''
    classdocs
    '''

    def __init__(self):
        self.pids = []
        self.cmds = {}
        self.cmds['run'] = self.run
        self.cmds['killall'] = self.killall

    def execute(self,cmd,param=''):
        if param == '':
            self.cmds[cmd]()
        else:
            self.cmds[cmd](param)

    def run(self,param):
        print 'run:',param
        p1 = subprocess.Popen(param, shell=False, stdin=None, stdout=None, stderr=None)
        self.pids.append(str(p1.pid))
        print 'pids:',self.pids
        print 'pid:',p1.pid,',return code:',p1.returncode
        
    def exit(self,pid):
        print('exit ',  os.getpid())
        pass
        sys.exit()
    
    def kill(self,pid):
        #os.kill(pid, 0)
        os._exit(0)
        print 'kill ',pid 
    
    def killall(self):
        killparam = self.pids
        sys = platform.system()
        if sys == 'Windows':
            i = 0
            while i < len(killparam):
                killparam.insert(i, '/PID')
                i+=2
            killparam.insert(0, '/F')
            killparam.insert(0, 'TASKKILL')
        else:
            killparam.insert(0, '-9')
            killparam.insert(0, 'kill')
        print 'killall:',killparam
        subprocess.Popen(killparam, shell=False, stdin=None, stdout=None, stderr=None)
    

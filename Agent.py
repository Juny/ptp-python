'''
@author: jun
'''
from common import Master
from common import Parser
from common import Server

if __name__ == '__main__':
    master = Master.Master()
    parser = Parser.CmdParser()
    agent = Server.AgentServer()
    agent.setMaster(master)
    agent.setParser(parser)
    agent.start(51888)
    print 'exit.'
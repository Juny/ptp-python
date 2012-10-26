
import thread
from common import Server
from common import Parser
from common import WebServer

#Agent
def startServer():
    parser = Parser.TransDataParser()
    controler = Server.ControlServer("d:\TestByGJY.db")
    controler.setParser(parser)
    controler.start(51999)

#Client
def startWebServer():
    server_address = ('', 8089)
    httpd = WebServer.PtpHttpServer(server_address, WebServer.PTPRequestHandler, "d:\TestByGJY.db", 'Control')
    httpd.serve_forever()
    
if __name__ == '__main__':
    thread.start_new_thread(startServer,())
    thread.start_new_thread(startWebServer,())
    input()

    
# Avg Max Min Last得内存算，数据库备份
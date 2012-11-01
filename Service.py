
import thread
from common import Server
from common import Parser
from common import WebServer

#Agent
def startServer(port=51999):
    parser = Parser.TransDataParser()
    controler = Server.ControlServer("d:\TestByGJY.db")
    controler.setParser(parser)
    controler.start(port)

#Client
def startWebServer(port=8089):
    server_address = ('', port)
    httpd = WebServer.PtpHttpServer(server_address, WebServer.PTPRequestHandler, "d:\TestByGJY.db", 'Control')
    httpd.serve_forever()
    
def startService(server_port, web_port):
    thread.start_new_thread(startServer,(server_port))
    thread.start_new_thread(startWebServer,(web_port))
    input()
    
if __name__ == '__main__':
    startService(51999,8089)

    
# Avg Max Min Last得内存算，数据库备份
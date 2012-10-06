'''
@author: jun
'''
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from common import Sqlite

class PTPRequestHandler(BaseHTTPRequestHandler):

    db = None
    processMethodDict = None
    
    def __init__(self, request, client_address, server):
        print 'PTPRequestHandler __init__'
        self.db = Sqlite.DbPorxy.getInstance(server.db_path)
        self.processMethodDict = {
                             '/test': self.procGetTest,
                             '/index': self.procGetIndex,
                             '/TransRspTime': self.getTransRspTime,
                             }
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

                
    def do_GET(self):
        print 'do_GET'
        path = self.path.split('.do')[0]
        if self.processMethodDict.has_key(path):
            self.processMethodDict[path]()
        else:
            self.send_error(404)
                
    def do_OPTIONS(self):
        print 'do_OPTIONS'
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:8080')
        self.send_header('Access-Control-Allow-Methods', 'POST,GET,OPTIONS')
        self.send_header('Access-Control-Max-Age', '300')
        self.end_headers()
        self.send_response(200)
#        path = self.path.split('.do')[0]
#        if self.processMethodDict.has_key(path):
#            self.processMethodDict[path](self)
#        else:
#            self.send_error(404)
            
    def do_SPAM(self):
        print 'do_SPAM'
        path = self.path.split('.do')[0]
        if self.processMethodDict.has_key(path):
            self.processMethodDict[path](self)
        else:
            self.send_error(404)


    def procGetTest(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('hi form test.')
    
    def procGetIndex(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('hi form index.')
    
    def getTransRspTime(self):
        self.send_response(200)
        if '?' in self.path:
            self.send_header('content-type', 'text/javascript')
            self.end_headers()
            self.wfile.write('Ext.data.JsonP.callback1(%s)' % self.db.executeSqlToJson("SELECT * FROM ResponseTime WHERE TranName = 'Reg3' limit 120"))
        else:
            self.send_header('content-type', 'application/x-json')
            self.end_headers()
            self.wfile.write(self.db.executeSqlToJson("SELECT * FROM ResponseTime WHERE TranName = 'Reg1' limit 2000"))

            
class PtpHttpServer(HTTPServer):
    db_path = None
    
    def __init__(self, server_address, RequestHandlerClass, db_path):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.db_path = db_path


if __name__ == '__main__':
    server_address = ('', 8089)
    httpd = PtpHttpServer(server_address, PTPRequestHandler, 'Test Path')
    httpd.serve_forever()

    
    
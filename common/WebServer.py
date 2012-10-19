'''
@author: jun
'''
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from common import Sqlite
from urlparse import urlparse

class PTPRequestHandler(BaseHTTPRequestHandler):

    db = None
    processMethodDict = None
    
    def __init__(self, request, client_address, server):
        print 'PTPRequestHandler __init__'
        self.db = Sqlite.DbPorxy.getInstance(server.db_path)
        self.processMethodDict = {
                             '/test': self.procGetTest,
                             '/index': self.procGetIndex,
                             '/TransTps': self.getTransTps,
                             '/TransTpsSummary': self.getTransTpsSummary,
                             '/TransRspTime': self.getTransRspTime,
                             '/TransRspTimeSummary': self.getTransRspTimeSummary,
                             }
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

                
    def do_GET(self):
        print 'do_GET.',self.path
        path = self.path.split('?')[0]
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
        #http://localhost:8089/TransRspTime.do?_dc=1349709497594&page=1&start=0&limit=25&callback=Ext.data.JsonP.callback1
        self.send_header('content-type', 'text/javascript')
        self.end_headers()
        callback = self.path.split('=')[-1]
        import random
        self.wfile.write('%s(%s)' % (callback,self.db.getResponseTimeWithJson('Test1','%s,%s'%(random.randint(0, 100),30) )))

    def getTransRspTimeSummary(self):
        self.send_response(200)
        #http://localhost:8089/TransRspTime.do?_dc=1349709497594&page=1&start=0&limit=25&callback=Ext.data.JsonP.callback1
        self.send_header('content-type', 'text/javascript')
        self.end_headers()
        callback = self.path.split('=')[-1]
        self.wfile.write('%s(%s)' % (callback,self.db.getTranRpsSummary()))
      
    def getTransTps(self):
        self.send_response(200)
        #http://localhost:8089/TransRspTime.do?_dc=1349709497594&page=1&start=0&limit=25&callback=Ext.data.JsonP.callback1
        self.send_header('content-type', 'text/javascript')
        self.end_headers()
        callback = self.path.split('=')[-1]
        import random
        self.wfile.write('%s(%s)' % (callback,self.db.getTranPerSecondWithJson('Test1','%s' % (random.randint(20, 50)))))

    def getTransTpsSummary(self):
        self.send_response(200)
        #http://localhost:8089/TransRspTime.do?_dc=1349709497594&page=1&start=0&limit=25&callback=Ext.data.JsonP.callback1
        self.send_header('content-type', 'text/javascript')
        self.end_headers()
        callback = self.path.split('=')[-1]
        self.wfile.write('%s(%s)' % (callback,self.db.getTranTpsSummary()))

            
class PtpHttpServer(HTTPServer):
    db_path = None
    control = None
    
    def __init__(self, server_address, RequestHandlerClass, db_path, control):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.db_path = db_path
        self.control = control

if __name__ == '__main__':
    server_address = ('', 8089)
    httpd = PtpHttpServer(server_address, PTPRequestHandler, "d:\TestByGJY.db")
    httpd.serve_forever()

    
    
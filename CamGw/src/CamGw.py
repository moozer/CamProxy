'''
Created on 28 Feb 2012

@author: moz

Basics mostly from the python docs
http://docs.python.org/library/simplehttpserver.html#module-SimpleHTTPServer

http://www.daniweb.com/software-development/python/threads/30410
'''
import SocketServer
from BaseHTTPServer import BaseHTTPRequestHandler
from WebTxVideo import WebTxVideo
import string

PORT = 8000
CamList = ['SamsungWebTx', 'b']



class CamGwHttpRequestHandler( BaseHTTPRequestHandler ):
    ''' Acts as authenticating gateway to samsung web tx boxes '''
    def do_GET(self):
#        try:
        CamName = string.lstrip( self.path, '/')
        if CamName in CamList:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            WebTx = WebTxVideo( CamName )
            while WebTx.DataAvailable():
                self.wfile.write( WebTx.read() )
                self.wfile.flush()
            return
        self.send_error(404,'File Not Found: %s' % self.path)            
#        except IOError as e:
#            print e
#            self.send_error(501,'Failed to forward request: %s' % CamName)
        
if __name__ == '__main__':
    Handler = CamGwHttpRequestHandler 
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    try:
        print "serving at port", PORT
        httpd.handle_request()
        #httpd.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        httpd.socket.close()
    pass
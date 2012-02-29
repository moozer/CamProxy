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
from TrendnetCamType import TrendnetCamType
import string

PORT = 8000
CamTypeList = ['WebTx', 'Trendnet']

class CamGwHttpRequestHandler( BaseHTTPRequestHandler ):
    ''' Acts as authenticating gateway to samsung web tx boxes '''
    def do_GET(self):
#        try:
        CameraString = string.lstrip(self.path, '/')
        CamType, CamName = string.split( CameraString, '/', 1)
        
        if CamType == 'WebTx':
            WebTx = WebTxVideo( CamName )
            
            self.send_response(200)
            self.send_header('Pragma', 'no-cache')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Content-type', 'multipart/x-mixed-replace;boundary=myboundary')
            self.end_headers()
            while WebTx.DataAvailable():
                self.wfile.write( WebTx.read() )
                self.wfile.flush()
            return
        
        elif CamType == 'Trendnet':
            TnCam = TrendnetCamType( CamName )

            self.send_response(200)
            BlackList = ['Server', 'Auther']
            headers = TnCam.GetHeaders()
            for header in headers.keys():
                if header in BlackList:
                    continue
                self.send_header( header, headers[header])
            self.end_headers()

            
            while TnCam.DataAvailable():
                self.wfile.write( TnCam.read() )
                #self.wfile.flush()
            return
    
        else:
            Mes  = 'Unknown Camera type: %s not in camera list\n' % CamType
            Mes += 'Try WebTx or Trendnet'
            self.send_error(404, Mes)            
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
    except Exception as e:
        print "something went wrong %s" % e
        

    httpd.socket.close()
    

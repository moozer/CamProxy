#!/usr/bin/python

'''
Created on 28 Feb 2012

@author: moz

References and inspiration
http://docs.python.org/library/simplehttpserver.html#module-SimpleHTTPServer
http://www.daniweb.com/software-development/python/threads/30410
http://www.doughellmann.com/PyMOTW/BaseHTTPServer/index.html#module-BaseHTTPServer


'''
import SocketServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from WebTxVideo import WebTxVideo
from TrendnetCamType import TrendnetCamType
import string
from SocketServer import ThreadingMixIn

PORT = 8001

HelpText = '''
Usage:
server:%d/<Camtype>/<host>

With Camtype being WebTx or Trendnet
and host is resolvable name to the camera

''' % (PORT)

class CamGwHttpRequestHandler( BaseHTTPRequestHandler ):
    ''' Acts as authenticating gateway to samsung web tx boxes and other cam types '''
    def do_GET(self):
#        try:
        CameraString = string.lstrip(self.path, '/')

        try:
            CamType, CamName = string.split( CameraString, '/', 1)
        except ValueError:
            Mes  = 'Failed to read Camtype\n'
            Mes += HelpText            
            self.send_error(404, Mes) 
            return

        if CamType == 'WebTx':
            CamObject = WebTxVideo( CamName )
            BlackList = ['Server', 'Auther', 'server']
        elif CamType == 'Trendnet':
            CamObject = TrendnetCamType( CamName )
            BlackList = ['server']
        else:
            Mes  = 'Unknown Camera type: %s not in camera list\n' % CamType
            Mes += HelpText
            self.send_error(404, Mes) 
            return
            
        # and pipe data based on camera object.
        self.send_response(200)
        headers = CamObject.GetHeaders()
        for header in headers.keys():
            if header in BlackList:
                continue
            self.send_header( header, headers[header])
        self.end_headers()

        while CamObject.DataAvailable():
            self.wfile.write( CamObject.read() )    
           
#        except IOError as e:
#            print e
#            self.send_error(501,'Failed to forward request: %s' % CamName)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    server = ThreadedHTTPServer(('', PORT), CamGwHttpRequestHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
    
#if __name__ == '__main__':
#    Handler = CamGwHttpRequestHandler 
#    httpd = SocketServer.TCPServer(("", PORT), Handler)
#    try:
#        print "serving at port", PORT
#        #httpd.handle_request()
#        httpd.serve_forever()
#    except KeyboardInterrupt:
#        print '^C received, shutting down server'
#    except Exception as e:
#        print "something went wrong %s" % e
#        
#    print "and closing socket"
#    httpd.socket.close()
    

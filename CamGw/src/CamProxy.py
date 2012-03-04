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
from WebTxVideoCamType import WebTxVideoCamType
from TrendnetCamType import TrendnetCamType
from FileCamType import FileCamType
import string
from SocketServer import ThreadingMixIn
import time
import sys


PORT = 8000

HelpText = '''
Usage:
server:%d/<Camtype>/<host>

With Camtype being File, WebTx or Trendnet
and host is resolvable name to the camera (or filename)

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

        try:
            if CamType == 'WebTx':
                CamObject = WebTxVideoCamType( CamName )
                BlackList = ['Server', 'server']
                ExtraHeaders = {}
            elif CamType == 'Trendnet':
                CamObject = TrendnetCamType( CamName )
                BlackList = ['server', 'content-type']
                ExtraHeaders = {'content-type': 'multipart/x-mixed-replace;boundary=%s'%CamObject.GetBoundary()}                
            elif CamType == 'File':
                CamObject = FileCamType( CamName )
                BlackList = []
                ExtraHeaders = {'content-type': 'multipart/x-mixed-replace;boundary=%s'%CamObject.GetBoundary()}                                
            else:
                Mes  = 'Unknown Camera type: %s not in camera list\n' % CamType
                Mes += HelpText
                self.send_error(404, Mes) 
                return
        except Exception as e:
            Mes  = 'Failed to initialize camera: %s\n' % CamName
            Mes += "Error: %s"%e
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
        for header in ExtraHeaders.keys():
            self.send_header( header, ExtraHeaders[header])
            
        self.end_headers()

        #self.wfile.write( "--%s--\r\n"%CamObject.GetBoundary() )
        while CamObject.DataAvailable():
            #write boundary
            self.wfile.write( CamObject.BoundaryText() )    
            self.wfile.write( CamObject.read() )
            self.wfile.write( "\r\n" )            
            sys.stderr.write(".")
            time.sleep( 0.1 )
           
        self.wfile.close()
#        except IOError as e:
#            print e
#            self.send_error(501,'Failed to forward request: %s' % CamName)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    DoMultiThreaded = True
    
    if DoMultiThreaded:
        server = ThreadedHTTPServer(('', PORT), CamGwHttpRequestHandler)
        print 'Starting server, use <Ctrl-C> to stop'
        server.serve_forever()
    else: # run once
        Handler = CamGwHttpRequestHandler 
        httpd = SocketServer.TCPServer(("", PORT), Handler)
        try:
            print "serving at port", PORT
            httpd.handle_request()
        except KeyboardInterrupt:
            print '^C received, shutting down server'
        except Exception as e:
            print "something went wrong %s" % e
            
        print "and closing socket"
        httpd.socket.close()
   

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

import syslog

PORT = 8000
BadDataCounterMax = 10

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
            Mes  = 'Failed to read Camtype\n%s'%HelpText
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
                Mes  = 'Unknown Camera type: %s not in camera list\n%s' % (CamType, HelpText)
                self.send_error(404, Mes) 
                return
        except Exception as e:
            Mes  = 'Failed to initialize camera: %s\nError: %s\n%s' % (CamName, e, HelpText)
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

        try:
            #self.wfile.write( "--%s--\r\n"%CamObject.GetBoundary() )
            while CamObject.DataAvailable():
                try:
                    #write boundary
                    self.wfile.write( CamObject.BoundaryText() )    
                    self.wfile.write( CamObject.read() )
                    self.wfile.write( "\r\n" )            
                    sys.stderr.write(".")
                    time.sleep( 0.1 )
                    BadDataCounter = 0

                except ValueError:
                    BadDataCounter += 1

                    if BadDataCounter > BadDataCounterMax:
                        raise ValueError( "%d bad images in sequence. Aborting"%BadDataCounter)
                        
                    sys.stderr.write("Bad data. Ignoring.\n")
                    self.log_message( "Bad data after %d images. Ignoring", CamObject.GetImageCount())
        except Exception as e:
            if e.errno == 32:
                mes = "Graceful client disconnect after %d images\n" % CamObject.GetImageCount()
                sys.stderr.write(mes)
            else:
                mes  = "Unhandled bad stuff after %d images\n" % CamObject.GetImageCount()
                mes += "Exception caught: %s " % e
                sys.stderr.write(mes)
                self.wfile.close()

            self.log_message( "Connection closed after %d images", CamObject.GetImageCount())
        CamObject.close()
#        except IOError as e:
#            print e
#            self.send_error(501,'Failed to forward request: %s' % CamName)

    def log_message(self, msg_format, *args ):
        DefMsg =  msg_format%args
        syslog.syslog( "%s"%DefMsg)
        sys.stderr.write( DefMsg )

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    syslog.syslog('CamProxy starting (port %d)'%PORT)
    
    DoMultiThreaded = True
    
    if DoMultiThreaded:
        server = ThreadedHTTPServer(('', PORT), CamGwHttpRequestHandler)
        print 'Starting server on port %d, use <Ctrl-C> to stop' % PORT
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
   
    syslog.syslog('CamProxy closed (port %d)'%PORT)

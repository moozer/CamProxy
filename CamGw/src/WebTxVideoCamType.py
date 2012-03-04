'''
Created on 28 Feb 2012

@author: moz

http://www.voidspace.org.uk/python/articles/authentication.shtml
'''

import urllib2
from CamType import CamType
import base64
import string

class WebTxVideoCamType( CamType ):
    '''
    classdocs
    '''
    def __init__(self, Servername ):
        self._ServerPath = "/video.cgi"
        self._Username = 'root'
        self._Password = 'root'
        self._ServerPath = '/cgi-bin/fwstream.cgi?ServerId=0&CameraId=1&FwCgiVer=0x0101&PauseTime=30'
                
        # inits other vars and calls _OpenHandle
        super(WebTxVideoCamType, self).__init__( Servername )
    
    def _OpenHandle(self):
        req = urllib2.Request('http://%s%s'%(self._ServerName, self._ServerPath))
        base64string = base64.encodestring('%s:%s' % (self._Username, self._Password))[:-1]
        req.add_header("Authorization", "Basic %s" % base64string)
        self._Handle = urllib2.urlopen(req)
        
        # TODO: get this from http headers.
        self._Boundary = "myboundary"
        
    def DataAvailable(self):
        return True
    
    def GetHeaders(self):
        return self._Handle.info().dict
    
        
    def _ReadMultipart(self ):
        ''' Read the first line and check if it matches the boundary
        camera doesn't send this line.
        '''
        pass
     
    def _ReadContentStrings(self):
        ''' read the boundary, content-length and content-type
        sets the self._NextImageLength based on content-length
        '''
        
        # we read the boundary at the end of an image in _Read
        if self._ImageCount == 0:
            self._HandleMultipartBoundary()
        #not supplying content length...
        #self._HandleContentLength()
        self._HandleContentType()

        # skip 'DaemonId' line
        self._Handle.readline()

        # and skip an empty line
        line = self._Handle.readline()
        if line != "\r\n":
            raise ValueError("Malformed mjpeg: missing empty line")
        
    def _ReadImage(self):
        ''' Read the next image. Default to reading the number of bytes defined
        by self._NextImageLength '''
        EndString =  "--%s\r\n"%self._Boundary
        ImgBuffer = ''
        for line in self._Handle:
            if line.endswith( EndString ):
                ImgBuffer += string.rstrip( line, EndString)
                return ImgBuffer
            else:
                ImgBuffer += line


         


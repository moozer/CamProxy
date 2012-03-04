'''
Created on 29 Feb 2012

@author: moz
'''

import urllib2
from CamType import CamType
import string 

class TrendnetCamType( CamType ):
    '''
    classdocs
    '''
    def __init__(self, Servername ):
        self._ServerPath = "/video.cgi"
        
        # inits other vars and calls _OpenHandle
        super(TrendnetCamType, self).__init__( Servername )
    
    def _OpenHandle(self):
        req = urllib2.Request('http://%s%s'%(self._ServerName, self._ServerPath))
        self._Handle = urllib2.urlopen(req)
        
        # TODO: get this from http headers.
        self._Boundary = "video boundary"
    
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
        
        rawline = self._HandleMultipartBoundary()

        if self._ImageCount > 0:
            self._HandleContentLength()
        else:
            # trendnet hack boundary and contenttype is on same line...
            line = string.rstrip(rawline)
            (typeid, value) = string.split( line, ": ", 1) #@UnusedVariable
            self._NextImageLength = int( value )
            
        # next line is the Content-type
        self._HandleContentType()

        # and an empty line
        line = self._Handle.readline()
        if line != "\r\n":
            raise ValueError("Malformed mjpeg: missing empty line")

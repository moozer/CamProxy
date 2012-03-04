'''
Created on 3 Mar 2012

@author: moz
'''

import string

class CamType(object):
    '''
    Superclass for handling mjpeg stuff.
    '''

    def __init__(self, Filename ):
        '''
        Constructor.
        Inits variables and open the handle to read from.
        '''
        self._ServerName = Filename
        self._Boundary = "ToBeSetLater"
        self._JpegContentType = "image/jpeg"
        self._ImageCount = 0
        self._NextImageLength = 0
        
        self._OpenHandle()
        
        # read first part of stream
        self._ReadMultipart()
        self._ReadContentStrings()
            
    def _OpenHandle(self):
        ''' function to be overloaded.
        Must set self._Handle to something appropriate '''
        pass
        
    def read(self):
        ''' Read from mjpeg and returns the next image '''
        Img = self._ReadImage()
        self._ImageCount = self._ImageCount +1
        self._ReadContentStrings()
        return Img

    def _ReadImage(self):
        ''' Read the next image. Default to reading the number of bytes defined
        by self._NextImageLength '''
        return self._Handle.read( self._NextImageLength )
         
    def _ReadMultipart(self ):
        ''' Read the first line and check if it matches the boundary '''
        # first line is the boundary definition tag line
        line = string.rstrip( self._Handle.readline() )
        if not line.startswith( "--%s"%self._Boundary ):
            raise ValueError( "Malformed mjpeg: Missing multipart start tag in line: %s"%line )
                   
    def _ReadContentStrings(self):
        ''' read the boundary, content-length and content-type
        sets the self._NextImageLength based on content-length
        '''
        # line is the image boundary
        rawline = self._Handle.readline()
        while rawline == '\r\n': # 
            rawline = self._Handle.readline()
        
        line = string.rstrip( rawline )
        if not line.startswith( "--%s"%self._Boundary ):
            raise ValueError( "Malformed mjpeg or EOF: Image boundary not found in line: %s"%line )
        
        # trendnet hack boundary and contenttype is on same line...
        # TODO: check on content-length
        if line == "--%s--"%self._Boundary: 
            line = string.rstrip( self._Handle.readline() )

        (type, value) = string.split( line, ": ", 1)
        self._NextImageLength = int( value )
            
        # next line is the Content-type
        line = string.rstrip( self._Handle.readline() )
        (type, value) = string.split( line, ": ", 1)

        if value != self._JpegContentType:
            raise ValueError( "Malformed mjpeg: bad content-type - expected '%s', got '%s'"%(self._JpegContentType, value) )

        # and an empty line
        line = self._Handle.readline()
        if line != "\r\n":
            raise ValueError("Malformed mjpeg: missing empty line")

           
    def BoundaryText(self):
        text  = "\r\n--%s\r\n"%self._Boundary
        #text += "Content-length: %d\r\n" % self._NextImageLength
        text += "Content-type: %s\r\n" %self._JpegContentType
        text += "\r\n"
        return text
    
    def GetBoundary(self):
        return self._Boundary
    
    def GetHeaders(self):
        return {'content-type': 'multipart/x-mixed-replace;boundary=%s'%self._Boundary }  
    
    def DataAvailable(self):
        return True  

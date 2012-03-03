'''
Created on 3 Mar 2012

@author: moz
'''

from CamType import CamType
import string

class FileCamType( CamType ):
    '''
    Test camera type to load from file
    '''


    def __init__(self, Filename, Boundary = "--video boundary"):
        '''
        Constructor
        '''
        self._ServerName = Filename
        self._Boundary = Boundary
        self._JpegContentType = "image/jpeg"
        
        self._OpenHandle()
        self._ImageCount = 0
        
        
    def _OpenHandle(self):
        self._Handle =  open( self._ServerName, "rb")
    
    def _CloseHandle(self):
        self._Handle.close()
        
    def _ReadFirstImage(self ):
        # first line is the boundary definition tag line
        line = string.rstrip( self._Handle.readline() )
        if not line.startswith( self._Boundary ):
            raise ValueError( "Malformed mjpeg: Missing multipart start tag" )
                   
    def _ReadContentStrings(self):      
        # line is the image boundary
        line = string.rstrip( self._Handle.readline() )
        if not line.startswith( self._Boundary ):
            raise ValueError( "Malformed mjpeg: First image boundary not found" )
        # trendnet hack boundary and contenttype is on same line...
        # TODO: check on content-length
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

    def _ReadImage(self):
        return self._Handle.read( self._NextImageLength )
         
           
    def read(self):
        ''' Read from mjpeg and returns the next image '''
        if self._ImageCount == 0:
            self._ReadFirstImage()
            self._ReadContentStrings()

        return self._ReadImage()
        


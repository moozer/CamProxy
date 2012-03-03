'''
Created on 3 Mar 2012

@author: moz
'''

from CamType import CamType
import string

class FileCamType( CamType ):
    '''
    Test camera type to load from file
    @param ServerName: the name of the mjpeg fil to open. 
    '''

    def _OpenHandle(self):
        self._Handle = open( self._ServerName+".mjpeg", "rb")
        
    def _ReadMultipart(self ):
        ''' Read the first line and extracts the boundary '''
        # first line is the boundary definition tag line
        line = string.rstrip( self._Handle.readline() )
        
        elements = string.split( line, "--")
        
        if len(elements) != 3:
            raise ValueError( "Malformed mjpeg: Unable to extract boundary from first line: %s" %line )

        self._Boundary = "--%s"%elements[1]

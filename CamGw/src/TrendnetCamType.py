'''
Created on 29 Feb 2012

@author: moz
'''

import urllib2
import string
import sys
from CamType import CamType

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
        
    def DataAvailable(self):
        return True
    
    def GetHeaders(self):
        return self._Handle.info().dict
    
    def _ReadMultipart(self ):
        ''' Read the first line and check if it matches the boundary
        Trendnet camera doesn't send this line.
        '''
        pass
     
       
 
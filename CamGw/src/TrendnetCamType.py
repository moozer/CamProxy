'''
Created on 29 Feb 2012

@author: moz
'''

import urllib2

class TrendnetCamType():
    '''
    classdocs
    '''

    def __init__( self, ServerName ):
        '''
        Constructor
        '''
        self._ServerName = ServerName
        self._ServerPath = '/video.cgi'
        
        req = urllib2.Request('http://%s%s'%(self._ServerName, self._ServerPath))
        self._Handle = urllib2.urlopen(req)
    
    def read(self, Chunksize = 1000):
        return self._Handle.read( Chunksize )
    
    def DataAvailable(self):
        return True
    
    def GetHeaders(self):
        return self._Handle.info().dict
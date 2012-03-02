'''
Created on 28 Feb 2012

@author: moz

http://www.voidspace.org.uk/python/articles/authentication.shtml
'''

import urllib2

class WebTxVideo():
    '''
    classdocs
    '''

    def __init__( self, ServerName ):
        '''
        Constructor
        '''
        self._Username = 'root'
        self._Password = 'root'
        self._ServerName = ServerName
        self._ServerPath = '/cgi-bin/fwstream.cgi?ServerId=0&CameraId=1&FwCgiVer=0x0101&PauseTime=30'
        
        req = urllib2.Request('http://%s%s'%(self._ServerName, self._ServerPath))

        import base64
        base64string = base64.encodestring('%s:%s' % (self._Username, self._Password))[:-1]
        req.add_header("Authorization", "Basic %s" % base64string)
        self._Handle = urllib2.urlopen(req)
    
    def read(self, Chunksize = 1000):
        return self._Handle.read( Chunksize )
    
    def DataAvailable(self):
        return True
    
    def GetHeaders(self):
        return self._Handle.info().dict
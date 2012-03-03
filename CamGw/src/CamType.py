'''
Created on 3 Mar 2012

@author: moz
'''

class CamType(object):
    '''
    Superclass for handling mjpeg stuff.
    '''


    def __init__(self, ServerName ):
        '''
        Constructor
        '''
        self._ServerName = ServerName

        
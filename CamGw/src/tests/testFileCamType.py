'''
Created on 3 Mar 2012

@author: moz
'''
import unittest

from FileCamType import FileCamType

MjpegFilename = "FormallyCorrectMjpeg.mjpg"

class Test(unittest.TestCase):

    def testInstantiate(self):
        FileCamType( MjpegFilename )
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
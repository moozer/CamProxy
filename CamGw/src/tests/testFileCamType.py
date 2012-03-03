'''
Created on 3 Mar 2012

@author: moz
'''
import unittest

from FileCamType import FileCamType

#MjpegFilename = "FormallyCorrectMjpeg.mjpg"
MjpegFilename = "FromTrendnet.mjpeg"
FirstJpegImage = "FirstImage.jpg"

class Test(unittest.TestCase):

    def testInstantiate(self):
        FileCamType( MjpegFilename )
        pass

    def testReadFirstImage(self):
        Cam = FileCamType( MjpegFilename )
        Img = Cam.read()
        KnownImg = open( FirstJpegImage ).read()
        
        self.assertEqual( Img, KnownImg )
        pass

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
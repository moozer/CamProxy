'''
Created on 3 Mar 2012

@author: moz
'''
import unittest

from FileCamType import FileCamType

#MjpegFilename = "FormallyCorrectMjpeg.mjpg"
MjpegFilename = "FromTrendnet"
JpegImage1 = "FirstImage.jpg"
JpegImage2 = "SecondImage.jpg"

class Test(unittest.TestCase):

    def testInstantiate(self):
        FileCamType( MjpegFilename )
        pass

    def testReadFirstImage(self):
        Cam = FileCamType( MjpegFilename )
        Img = Cam.read()
        KnownImg = open( JpegImage1 ).read()
        self.assertEqual( Img, KnownImg )
        pass

    def testReadTwoImages(self):
        Cam = FileCamType( MjpegFilename )
        Cam.read()
        Img = Cam.read()
        KnownImg = open( JpegImage2 ).read()
        self.assertEqual( Img, KnownImg )
        pass

    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
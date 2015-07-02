import unittest

from helpers._os_lib import runAUT
from helpers._tns_lib import tnsPath
class Doctor(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):        
        pass

    def test_001_Version(self):
        output = runAUT(tnsPath + " doctor")
        assert ("No issues were detected." in output)
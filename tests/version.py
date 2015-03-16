import re
import unittest

from helpers._os_lib import runAUT
from helpers._tns_lib import tnsPath

class Version(unittest.TestCase):
    
    def setUp(self):
        
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):        
        pass

    def test_010_Version(self):
        output = runAUT(tnsPath + " --version")
        a = re.compile('^\d+\.\d+\.\d+(-\d+)?$')
        assert (a.match(output))
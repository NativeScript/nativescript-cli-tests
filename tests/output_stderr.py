import os, unittest

from helpers._os_lib import remove, runAUT
from helpers._tns_lib import tnsPath

class Output_STRERR(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        remove('stderr.txt');

    def tearDown(self):
        remove('stderr.txt');

    def test_001_Output_STRERR(self):
        os.system(tnsPath + " emulate asdf 2>stderr.txt")
        output = runAUT("cat stderr.txt")
        assert ("The input is not valid sub-command for 'emulate' command" in output)
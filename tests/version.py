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

    def test_001_Version(self):
        output = runAUT(tnsPath + " --version")
        isValidVersion = re.compile('^\d+\.\d+\.\d+(-\S+)?$').match(output);
        assert (isValidVersion), "Not a valid version"

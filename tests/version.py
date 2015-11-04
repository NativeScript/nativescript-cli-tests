import re, unittest

from helpers._os_lib import runAUT
from helpers._tns_lib import tnsPath

# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0111, R0201


class Version(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_version(self):
        output = runAUT(tnsPath + " --version")
        is_valid_version = re.compile("^\d+\.\d+\.\d+(-\S+)?$").match(output)
        assert (is_valid_version), "Not a valid version."

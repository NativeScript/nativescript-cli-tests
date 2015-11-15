'''
Test for doctor command
'''
import platform
import unittest

from helpers._os_lib import run_aut
from helpers._tns_lib import TNS_PATH


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class Doctor(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_doctor(self):
        output = run_aut(TNS_PATH + " doctor")

        # Ignore this check on Windows and Linux because of
        # https://github.com/NativeScript/nativescript-cli/issues/615
        if 'Darwin' in platform.platform():
            assert "No issues were detected." in output
        else:
            pass

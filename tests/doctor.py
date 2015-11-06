import platform
import unittest

from helpers._os_lib import run_aut
from helpers._tns_lib import TNSPATH

# pylint: disable=R0201, C0111


class Doctor(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_Doctor(self):
        output = run_aut(TNSPATH + " doctor")

        # Ignore this check on Windows and Linux because of
        # https://github.com/NativeScript/nativescript-cli/issues/615
        if 'Darwin' in platform.platform():
            assert "No issues were detected." in output
        else:
            pass

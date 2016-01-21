"""
Test for Android debugger
"""
import unittest

# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=R0201, C0103, C0111, R0904
from core.osutils.folder import Folder


class DebugAndroid(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    @unittest.skip("Not implemented.")
    def test_001_debug_android(self):
        # TODO: Implement this test
        pass

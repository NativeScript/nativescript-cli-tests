"""
Test for Android debugger
"""
import unittest
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

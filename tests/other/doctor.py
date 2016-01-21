"""
Test for doctor command
"""

import unittest

from core.osutils.command import run
from core.settings.settings import TNS_PATH, OSType, CURRENT_OS


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
        output = run(TNS_PATH + " doctor")

        # Ignore this check on Windows and Linux because of
        # https://github.com/NativeScript/nativescript-cli/issues/615
        if CURRENT_OS == OSType.OSX:
            assert "No issues were detected." in output
        else:
            pass

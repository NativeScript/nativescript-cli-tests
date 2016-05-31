"""
Test for doctor command
"""

import unittest

from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import TNS_PATH, OSType, CURRENT_OS
from core.tns.tns import Tns


class Doctor(unittest.TestCase):
    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    # Ignore this check on Windows and Linux because of
    # https://github.com/NativeScript/nativescript-cli/issues/615
    @unittest.skipIf(CURRENT_OS != OSType.OSX, "Not on OSX")
    def test_001_doctor(self):
        output = run(TNS_PATH + " doctor")
        assert "No issues were detected." in output


    def test_200_doctor_show_warning_when_new_components_are_available(self):
        Tns.create_app_platform_add(
            app_name="TNS_App",
            platform="android@1.7.0")
        output = run(TNS_PATH + " doctor --path TNS_App")
        assert "Updates available" in output
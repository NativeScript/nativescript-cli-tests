"""
Test for doctor command
"""

import unittest

from core.osutils.folder import Folder
from core.tns.tns import Tns


class Doctor_Tests(unittest.TestCase):
    app_name = "TNS_App"

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./' + self.app_name)

    def tearDown(self):
        pass

    def test_001_doctor(self):
        output = Tns.run_tns_command("doctor", timeout=180)
        assert "No issues were detected." in output

    def test_200_doctor_show_warning_when_new_components_are_available(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(version="1.7.0", attributes={"--path": self.app_name})
        output = Tns.run_tns_command("doctor", attributes={"--path": self.app_name}, timeout=180)
        assert "Updates available" in output

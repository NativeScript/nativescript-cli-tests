"""
Tests for doctor command
"""
import unittest

from core.base_class.BaseClass import BaseClass
from core.osutils.os_type import OSType
from core.settings.settings import CURRENT_OS
from core.settings.strings import *
from core.tns.tns import Tns


class DoctorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    @unittest.skipIf(CURRENT_OS != OSType.OSX,
                     "Ignore because of https://github.com/NativeScript/nativescript-cli/issues/3413")
    def test_001_doctor(self):
        output = Tns.run_tns_command("doctor", timeout=180)
        assert no_issues in output

    def test_200_doctor_show_warning_when_new_components_are_available(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(version="2.2.0", attributes={"--path": self.app_name})
        output = Tns.run_tns_command("doctor", attributes={"--path": self.app_name}, timeout=180)
        assert "Updates available" in output

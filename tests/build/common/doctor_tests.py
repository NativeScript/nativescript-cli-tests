"""
Tests for doctor command
"""

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.settings.strings import *


class DoctorTests(BaseClass):
    def test_001_doctor(self):
        output = Tns.run_tns_command("doctor", timeout=180)
        assert no_issues in output

    def test_200_doctor_show_warning_when_new_components_are_available(self):
        Tns.create_app(self.app_name, update_modules=False)
        Tns.platform_add_android(version="2.2.0", attributes={"--path": self.app_name})
        output = Tns.run_tns_command("doctor", attributes={"--path": self.app_name}, timeout=180)
        assert updates_available in output

"""
Tests redirecting error log
"""

from core.osutils.file import File
from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.settings.strings import *


class OutputStderrTests(BaseClass):
    def test_001_output_strerr(self):
        File.remove('./stderr.txt')
        output = Tns.run_tns_command(emulate + " " + invalid, attributes={" 2> stderr.txt ": ""})
        assert invalid_input.format(emulate) in output

    def test_002_command_option_validation(self):
        output = Tns.run_tns_command("create " + self.app_name_dash, attributes={"--" + invalid: "tns-app"})
        assert invalid_option.format(invalid) in output

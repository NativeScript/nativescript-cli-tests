"""
Tests redirecting error log and command options validations.
"""

from core.osutils.file import File
from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.settings.strings import *
import time


class OutputStderrTests(BaseClass):
    def tearDown(self):
        print ""
        print "{0} ____________________________________TEST END____________________________________". \
            format(time.strftime("%X"))
        print ""

    def test_001_output_strerr(self):
        File.remove('./stderr.txt')
        output = Tns.run_tns_command(run + " " + invalid, attributes={" 2> stderr.txt ": ""})
        assert invalid_input.format(run) in output

    def test_002_command_option_validation(self):
        output = Tns.run_tns_command("create " + self.app_name, attributes={"--" + invalid: "tns-app"})
        assert invalid_option.format(invalid) in output

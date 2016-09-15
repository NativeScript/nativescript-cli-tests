"""
Tests redirecting error log
"""

from core.osutils.file import File
from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass



class OutputStderr_Tests(BaseClass):
    def test_001_output_strerr(self):
        File.remove('./stderr.txt')
        Tns.run_tns_command("emulate asdf", attributes={" 2> stderr.txt ": ""})
        assert "The input is not valid sub-command for 'emulate' command" in output

    def test_002_command_option_validation(self):
        output = Tns.run_tns_command("create " + self.app_name_dash, attributes={"--abc": "tns-app"})
        assert "The option 'abc' is not supported. " in output

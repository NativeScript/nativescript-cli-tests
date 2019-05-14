"""
Tests for error output.
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.tns.tns import Tns


class StderrOutputTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_001_redirect_strerr_output_to_file(self):
        File.remove('./stderr.txt')
        output = Tns.run_tns_command("run invalidEntry", attributes={" 2> stderr.txt ": ""})
        assert "The input is not valid sub-command for 'run' command" in output

    def test_002_command_option_validation(self):
        output = Tns.run_tns_command("create " + self.app_name, attributes={"--invalidEntry": "tns-app"})
        assert "The option 'invalidEntry' is not supported." in output

"""
Tests for error output.
"""

from core.base_class.BaseClass import BaseClass
from core.osutils.file import File
from core.settings.strings import invalid, invalid_input, invalid_option
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
        output = Tns.run_tns_command("run " + invalid, attributes={" 2> stderr.txt ": ""})
        assert invalid_input.format("run") in output

    def test_002_command_option_validation(self):
        output = Tns.run_tns_command("create " + self.app_name, attributes={"--" + invalid: "tns-app"})
        assert invalid_option.format(invalid) in output

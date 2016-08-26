"""
Test redirecting error log
"""
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.settings.settings import TNS_PATH
from core.tns.tns import Tns



class OutputStderr_Tests(unittest.TestCase):
    app_name = "tns-app"

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        File.remove('./stderr.txt')

    def tearDown(self):
        File.remove('./stderr.txt')

    def test_001_output_strerr(self):
        output = Tns.run_tns_command("emulate asdf", attributes={" 2> stderr.txt ": ""})

        assert "The input is not valid sub-command for 'emulate' command" in output

    def test_002_command_option_validation(self):
        output = Tns.run_tns_command("create " + self.app_name, attributes={"--abc": "tns-app"})
        assert "The option 'abc' is not supported. " in output

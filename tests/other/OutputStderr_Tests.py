"""
Test redirecting error log
"""
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.settings.settings import TNS_PATH


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
        run(TNS_PATH + " emulate asdf", file_name="stderr.txt")
        output = run("cat stderr.txt")
        assert "The input is not valid sub-command for 'emulate' command" in output

    def test_002_command_option_validation(self):
        output = Tns.create_app(self.app_name, attributes={"--Copy-From": "tns-app"}, assert_success=False)
        assert "The option 'Copy-From' is not supported. " in output

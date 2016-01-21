"""
Test redirecting error log
"""
import unittest

from core.osutils.command import run
from core.osutils.file import File
from core.settings.settings import TNS_PATH


class Output_STRERR(unittest.TestCase):
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
        output = run(TNS_PATH + " create tns-app --Copy-From tns-app")
        assert "The option 'Copy-From' is not supported. " in output

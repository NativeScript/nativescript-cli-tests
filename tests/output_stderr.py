'''
Test redirecting error log
'''
import os
import unittest

from helpers._os_lib import remove, run_aut
from helpers._tns_lib import TNSPATH

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0103, C0111, R0201
class Output_STRERR(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        remove('stderr.txt')

    def tearDown(self):
        remove('stderr.txt')

    def test_001_output_strerr(self):
        os.system(TNSPATH + " emulate asdf 2>stderr.txt")
        output = run_aut("cat stderr.txt")
        assert "The input is not valid sub-command for 'emulate' command" in output

    def test_002_command_option_validation(self):
        output = run_aut(TNSPATH + " create tns-app --Copy-From tns-app")
        assert "The option 'Copy-From' is not supported. " in output

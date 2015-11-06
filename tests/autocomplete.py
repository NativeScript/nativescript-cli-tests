'''
Autocomplete tests
'''
import unittest

from helpers._os_lib import run_aut
from helpers._tns_lib import tnsPath

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0915 - Too many statements
# pylint: disable=R0201, R0915, C0111, C0103


class Autocomplete(unittest.TestCase):

    '''
    Autocomplete tests
    '''

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_autocomplete_enable(self):
        output = run_aut(tnsPath + " autocomplete status")
        if "Autocompletion is disabled." in output:
            output = run_aut(tnsPath + " autocomplete enable --log trace")
            assert "Restart your shell to enable command auto-completion." in output
        else:
            output = run_aut(tnsPath + " autocomplete enable --log trace")
            assert "Autocompletion is already enabled." in output
        output = run_aut(tnsPath + " autocomplete status")
        assert "Autocompletion is enabled." in output

    def test_002_autocomplete_disable(self):
        output = run_aut(tnsPath + " autocomplete status")
        if "Autocompletion is enabled." in output:
            output = run_aut(tnsPath + " autocomplete disable")
            assert "Restart your shell to disable command auto-completion." in output
        else:
            output = run_aut(tnsPath + " autocomplete disable")
            assert "Autocompletion is already disabled." in output
        output = run_aut(tnsPath + " autocomplete status")
        assert "Autocompletion is disabled." in output

    def test_400_autocomplete_invalid_parameter(self):
        command = tnsPath + " autocomplete invalidParam"
        output = run_aut(command)
        assert "The input is not valid sub-command for 'autocomplete' command" in output

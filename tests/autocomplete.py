'''
Autocomplete tests
'''
import unittest

from helpers._os_lib import runAUT
from helpers._tns_lib import tnsPath

# pylint: disable=R0201, C0111, C0103
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
        output = runAUT(tnsPath + " autocomplete status")
        if "Autocompletion is disabled." in output:
            output = runAUT(tnsPath + " autocomplete enable --log trace")
            assert "Restart your shell to enable command auto-completion." in output
        else:
            output = runAUT(tnsPath + " autocomplete enable --log trace")
            assert "Autocompletion is already enabled." in output
        output = runAUT(tnsPath + " autocomplete status")
        assert "Autocompletion is enabled." in output

    def test_002_autocomplete_disable(self):
        output = runAUT(tnsPath + " autocomplete status")
        if "Autocompletion is enabled." in output:
            output = runAUT(tnsPath + " autocomplete disable")
            assert "Restart your shell to disable command auto-completion." in output
        else:
            output = runAUT(tnsPath + " autocomplete disable")
            assert "Autocompletion is already disabled." in output
        output = runAUT(tnsPath + " autocomplete status")
        assert "Autocompletion is disabled." in output

    def test_400_autocomplete_invalid_parameter(self):
        command = tnsPath + " autocomplete invalidParam"
        output = runAUT(command)
        assert "The input is not valid sub-command for 'autocomplete' command" in output

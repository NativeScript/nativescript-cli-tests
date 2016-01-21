"""
Autocomplete tests
"""

import unittest

from core.osutils.command import run
from core.settings.settings import TNS_PATH


class Autocomplete(unittest.TestCase):
    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_autocomplete_enable(self):
        output = run(TNS_PATH + " autocomplete status")
        if "Autocompletion is disabled." in output:
            output = run(TNS_PATH + " autocomplete enable --log trace")
            assert "Restart your shell to enable command auto-completion." in output
        else:
            output = run(TNS_PATH + " autocomplete enable --log trace")
            assert "Autocompletion is already enabled." in output
        output = run(TNS_PATH + " autocomplete status")
        assert "Autocompletion is enabled." in output

    def test_002_autocomplete_disable(self):
        output = run(TNS_PATH + " autocomplete status")
        if "Autocompletion is enabled." in output:
            output = run(TNS_PATH + " autocomplete disable")
            assert "Restart your shell to disable command auto-completion." in output
        else:
            output = run(TNS_PATH + " autocomplete disable")
            assert "Autocompletion is already disabled." in output
        output = run(TNS_PATH + " autocomplete status")
        assert "Autocompletion is disabled." in output

    def test_400_autocomplete_invalid_parameter(self):
        command = TNS_PATH + " autocomplete invalidParam"
        output = run(command)
        assert "The input is not valid sub-command for 'autocomplete' command" in output

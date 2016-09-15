"""
Autocomplete tests
"""

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass


class Autocomplete_Tests(BaseClass):

    def test_001_autocomplete_enable(self):
        output = Tns.run_tns_command("autocomplete status")
        if "Autocompletion is disabled." in output:
            output = Tns.run_tns_command("autocomplete enable", log_trace=True)
            assert "Restart your shell to enable command auto-completion." in output
        else:
            output = Tns.run_tns_command("autocomplete enable", log_trace=True)
            assert "Autocompletion is already enabled." in output
        output = Tns.run_tns_command("autocomplete status")
        assert "Autocompletion is enabled." in output

    def test_002_autocomplete_disable(self):
        output = Tns.run_tns_command("autocomplete status")
        if "Autocompletion is enabled." in output:
            output = Tns.run_tns_command("autocomplete disable", log_trace=True)
            assert "Restart your shell to disable command auto-completion." in output
        else:
            output = Tns.run_tns_command("autocomplete disable", log_trace=True)
            assert "Autocompletion is already disabled." in output
        output = Tns.run_tns_command("autocomplete status")
        assert "Autocompletion is disabled." in output

    def test_400_autocomplete_invalid_parameter(self):
        output = Tns.run_tns_command("autocomplete invalidParam")
        assert "The input is not valid sub-command for 'autocomplete' command" in output

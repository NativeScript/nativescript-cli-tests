"""
Autocomplete tests
"""

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.settings.strings import *


class AutocompleteTests(BaseClass):

    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass(cls.__name__)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()

    def test_101_autocomplete_enable(self):
        output = Tns.run_tns_command(autocomplete + " status")
        if disabled.format(autocompletion, "") in output:
            output = Tns.run_tns_command(autocomplete + " enable", log_trace=True)
            assert restart_shell.format("enable") in output
        else:
            output = Tns.run_tns_command(autocomplete + " enable", log_trace=True)
            assert enabled.format(autocompletion, "already ") in output
        output = Tns.run_tns_command(autocomplete + " status")
        assert enabled.format(autocompletion, "") in output

    def test_102_autocomplete_disable(self):
        output = Tns.run_tns_command(autocomplete + " status")
        if enabled.format(autocompletion, "") in output:
            output = Tns.run_tns_command(autocomplete + " disable", log_trace=True)
            assert restart_shell.format("disable") in output
        else:
            output = Tns.run_tns_command(autocomplete + " disable", log_trace=True)
            assert enabled.format(autocompletion, "already ") in output
        output = Tns.run_tns_command(autocomplete + " status")
        assert disabled.format(autocompletion, "") in output

    def test_400_autocomplete_invalid_parameter(self):
        output = Tns.run_tns_command(autocomplete + " " + invalid)
        assert invalid_input.format(autocomplete) in output

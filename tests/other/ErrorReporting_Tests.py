"""
Test for error-reporting command
"""

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass


class ErrorReporting_Tests(BaseClass):
    def test_001_error_reporting(self):
        output = Tns.run_tns_command("error-reporting")
        assert "Error reporting is" in output

    def test_002_error_reporting_enable(self):
        output = Tns.run_tns_command("error-reporting enable")
        assert "Error reporting is now enabled." in output

        output = Tns.run_tns_command("error-reporting status")
        assert "Error reporting is enabled." in output

    def test_003_error_reporting_disable(self):
        output = Tns.run_tns_command("error-reporting disable")
        assert "Error reporting is now disabled." in output

        output = Tns.run_tns_command("error-reporting status")
        assert "Error reporting is disabled." in output

    def test_401_error_reporting_with_invalid_parameter(self):
        output = Tns.run_tns_command("error-reporting invalidParam")
        assert "The value 'invalidParam' is not valid. " + \
               "Valid values are 'enable', 'disable' and 'status'" in output

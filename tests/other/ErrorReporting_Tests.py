"""
Test for error-reporting command
"""

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.settings.strings import *


class ErrorReportingTests(BaseClass):
    def test_001_error_reporting_enable(self):
        output = Tns.run_tns_command(errorreporting + " enable")
        assert enabled.format(error_reporting, "now ") in output

        output = Tns.run_tns_command(errorreporting + " status")
        assert enabled.format(error_reporting, "") in output

    def test_002_error_reporting_disable(self):
        output = Tns.run_tns_command(errorreporting + " disable")
        assert disabled.format(error_reporting, "now ") in output

        output = Tns.run_tns_command(errorreporting + " status")
        assert disabled.format(error_reporting, "") in output

    def test_401_error_reporting_with_invalid_parameter(self):
        output = Tns.run_tns_command(errorreporting + " " + invalid)
        assert invalid_value.format(invalid) in output

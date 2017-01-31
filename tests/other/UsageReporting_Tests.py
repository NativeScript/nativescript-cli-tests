"""
Test for usage-reporting command
"""

from core.tns.tns import Tns
from core.base_class.BaseClass import BaseClass
from core.settings.strings import *


class UsageReportingTests(BaseClass):
    def test_001_usage_reporting_enable(self):
        output = Tns.run_tns_command("usage-reporting enable")
        assert enabled.format(usage_reporting, "now ") in output

        output = Tns.run_tns_command("usage-reporting status")
        assert enabled.format(usage_reporting, "") in output

    def test_002_usage_reporting_disable(self):
        output = Tns.run_tns_command("usage-reporting disable")
        assert disabled.format(usage_reporting, "now ") in output

        output = Tns.run_tns_command("usage-reporting status")
        assert disabled.format(usage_reporting, "") in output

    def test_401_usage_reporting_with_invalid_parameter(self):
        output = Tns.run_tns_command("usage-reporting " + invalid)
        assert invalid_value.format(invalid) in output

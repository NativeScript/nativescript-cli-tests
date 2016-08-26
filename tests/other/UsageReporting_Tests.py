"""
Test for usage-reporting command
"""

import unittest
from core.tns.tns import Tns


class UsageReporting_Tests(unittest.TestCase):
    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_usage_reporting(self):
        output = Tns.run_tns_command("usage-reporting")
        assert "Usage reporting is" in output

    def test_002_usage_reporting_enable(self):
        output = Tns.run_tns_command("usage-reporting enable")
        assert "Usage reporting is now enabled." in output

        output = Tns.run_tns_command("usage-reporting status")
        assert "Usage reporting is enabled." in output

    def test_003_usage_reporting_disable(self):
        output = Tns.run_tns_command("usage-reporting disable")
        assert "Usage reporting is now disabled." in output

        output = Tns.run_tns_command("usage-reporting status")
        assert "Usage reporting is disabled." in output

    def test_401_usage_reporting_with_invalid_parameter(self):
        output = Tns.run_tns_command("usage-reporting invalidParam")
        assert "The value 'invalidParam' is not valid. " + \
               "Valid values are 'enable', 'disable' and 'status'" in output

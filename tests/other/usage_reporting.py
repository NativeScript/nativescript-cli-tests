"""
Test for usage-reporting command
"""

import unittest

from core.osutils.command import run
from core.settings.settings import TNS_PATH


class Usage(unittest.TestCase):
    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_usage_reporting(self):
        output = run(TNS_PATH + " usage-reporting")
        assert "Usage reporting is" in output

    def test_002_usage_reporting_enable(self):
        output = run(TNS_PATH + " usage-reporting enable")
        assert "Usage reporting is now enabled." in output

        output = run(TNS_PATH + " usage-reporting status")
        assert "Usage reporting is enabled." in output

    def test_003_usage_reporting_disable(self):
        output = run(TNS_PATH + " usage-reporting disable")
        assert "Usage reporting is now disabled." in output

        output = run(TNS_PATH + " usage-reporting status")
        assert "Usage reporting is disabled." in output

    def test_401_usage_reporting_with_invalid_parameter(self):
        command = TNS_PATH + " usage-reporting invalidParam"
        output = run(command)
        assert "The value 'invalidParam' is not valid. " + \
               "Valid values are 'enable', 'disable' and 'status'" in output

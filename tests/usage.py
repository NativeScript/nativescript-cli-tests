'''
Test for usage* commands
'''
import unittest

from helpers._os_lib import run_aut
from helpers._tns_lib import TNSPATH


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class UsageAndErrorTracking(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    def test_001_feature_usage_tracking(self):
        output = run_aut(TNSPATH + " usage-reporting")
        assert "Usage reporting is" in output

    def test_002_feature_usage_tracking_enable(self):
        output = run_aut(TNSPATH + " usage-reporting enable")
        assert "Usage reporting is now enabled." in output

        output = run_aut(TNSPATH + " usage-reporting status")
        assert "Usage reporting is enabled." in output

    def test_003_feature_usage_tracking_disable(self):
        output = run_aut(TNSPATH + " usage-reporting disable")
        assert "Usage reporting is now disabled." in output

        output = run_aut(TNSPATH + " usage-reporting status")
        assert "Usage reporting is disabled." in output

    def test_100_error_reporting(self):
        output = run_aut(TNSPATH + " error-reporting")
        assert "Error reporting is" in output

    def test_101_error_reporting_enable(self):
        output = run_aut(TNSPATH + " error-reporting enable")
        assert "Error reporting is now enabled." in output

        output = run_aut(TNSPATH + " error-reporting status")
        assert "Error reporting is enabled." in output

    def test_102_error_reporting_disable(self):
        output = run_aut(TNSPATH + " error-reporting disable")
        assert "Error reporting is now disabled." in output

        output = run_aut(TNSPATH + " error-reporting status")
        assert "Error reporting is disabled." in output

    def test_400_feature_usage_tracking_with_invalid_parameter(self):
        command = TNSPATH + " usage-reporting invalidParam"
        output = run_aut(command)
        assert "The value 'invalidParam' is not valid. " + \
            "Valid values are 'enable', 'disable' and 'status'" in output

    def test_401_error_reporting_with_invalid_parameter(self):
        command = TNSPATH + " error-reporting invalidParam"
        output = run_aut(command)
        assert "The value 'invalidParam' is not valid. " + \
            "Valid values are 'enable', 'disable' and 'status'" in output

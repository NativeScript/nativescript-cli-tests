'''
log_trace tests
'''
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import create_project, TNS_PATH


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class LogTrace(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_create_project_log_trace(self):
        output = run_aut(TNS_PATH + " create TNS_App --log trace")
        assert "Creating a new NativeScript project with name TNS_App" in output
        assert "and id org.nativescript.TNSApp at location" in output

        assert "Using NativeScript verified template:" in output
        assert "tns-template-hello-world with version undefined." in output

        assert "Copying application from" in output
        assert "Updating AppResources values" in output
        assert "Project TNS_App was successfully created" in output

    def test_002_platform_add_log_trace(self):
        create_project(proj_name="TNS_App")
        output = run_aut(TNS_PATH + " platform add android --path TNS_App --log trace")
        assert "Looking for project in" in output
        assert "Project directory is" in output
        assert "Package: org.nativescript.TNSApp" in output
        assert "Available Android targets" in output
        assert "Using Android SDK" in output
        assert "Project successfully created" in output

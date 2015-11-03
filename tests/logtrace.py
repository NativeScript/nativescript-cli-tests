import unittest

from helpers._os_lib import runAUT, CleanupFolder
from helpers._tns_lib import tnsPath, CreateProject

# pylint: disable=R0201, C0111
class LogTrace(unittest.TestCase):

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')

    def tearDown(self):
        pass

    def test_001_Create_Project_LogTrace(self):
        output = runAUT(tnsPath + " create TNS_App --log trace")
        assert "Creating a new NativeScript project with name TNS_App and id org.nativescript.TNSApp at location" in output
        assert "Using NativeScript hello world application" in output
        assert "Copying NativeScript hello world application into" in output
        assert "Project TNS_App was successfully created" in output

    def test_002_Platform_Add_LogTrace(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " platform add android --path TNS_App --log trace")
        assert "Looking for project in" in output
        assert "Project directory is" in output
        assert "Package: org.nativescript.TNSApp" in output
        assert "Available Android targets" in output
        assert "using Android SDK '" in output

        assert "Project successfully created" in output

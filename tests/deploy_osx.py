'''
Test for deploy command
'''
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProject, CreateProjectAndAddPlatform, \
    iosRuntimeSymlinkPath, tnsPath
from helpers.device import GivenRealDeviceRunning

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=R0201, C0111, R0904
class DeployiOS(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        GivenRealDeviceRunning(platform="ios")

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_App')

    def tearDown(self):
        CleanupFolder('./TNS_App')

    @classmethod
    def tearDownClass(cls):
        pass

    def test_001_Deploy_iOS_Device(self):
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="ios",
            frameworkPath=iosRuntimeSymlinkPath,
            symlink=True)
        output = runAUT(tnsPath + " deploy ios --path TNS_App  --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_200_Deploy_iOS_PlatformNotAdded(self):
        CreateProject(projName="TNS_App")
        output = runAUT(tnsPath + " deploy ios --path TNS_App --justlaunch")
        assert "Copying template files..." in output
        assert "Project successfully created." in output

        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProjectAndAddPlatform, androidRuntimePath, \
    tnsPath, androidKeyStorePath, androidKeyStorePassword, androidKeyStoreAlias, \
    androidKeyStoreAliasPassword, CreateProject
from helpers.device import GivenRunningEmulator, GivenRealDeviceRunning

# pylint: disable=R0201, C0111
class Deploy_Linux(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanupFolder('./TNS_App')
        CreateProjectAndAddPlatform(projName="TNS_App", platform="android", frameworkPath=androidRuntimePath)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        CleanupFolder('./TNS_AppNoPlatform')
        GivenRunningEmulator()
        GivenRealDeviceRunning(platform="android")
        CleanupFolder('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        CleanupFolder('./TNS_App')

    def test_001_Deploy_Android(self):
        output = runAUT(tnsPath + " deploy android --path TNS_App  --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is running on this device

    def test_002_Deploy_Android_ReleaseConfiguration(self):
        output = runAUT(tnsPath + " deploy android --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is running on this device

    def test_200_Deploy_Android_DeviceId(self):
        output = runAUT(tnsPath + " deploy android --device emulator-5554 --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        # TODO: Get device id and verify files are deployed and process is running on this device

    def test_201_Deploy_Android_InsideProject(self):
        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) + " deploy android --path TNS_App --justlaunch")
        os.chdir(currentDir);
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_210_Deploy_Android_PlatformNotAdded(self):
        CreateProject(projName="TNS_AppNoPlatform")
        output = runAUT(tnsPath + " deploy android --path TNS_AppNoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is running on this device

    def test_401_Deploy_InvalidPlatform(self):
        output = runAUT(tnsPath + " deploy invalidPlatform --path TNS_App --justlaunch")
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output

    def test_402_Deploy_InvalidDevice(self):
        output = runAUT(tnsPath + " deploy android --device invalidDeviceId --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Cannot resolve the specified connected device by the provided index or identifier" in output
        assert "To list currently connected devices and verify that the specified index or identifier exists, run 'tns device'" in output

import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProject, CreateProjectAndAddPlatform, \
    tnsPath, androidKeyStorePath, androidKeyStorePassword, \
    androidKeyStoreAlias, androidKeyStoreAliasPassword, androidRuntimePath
from helpers.device import GivenRunningEmulator, GivenRealDeviceRunning

# pylint: disable=R0201, C0111


class Run_Linux(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanupFolder('./TNS_App')
        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="android",
            frameworkPath=androidRuntimePath)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        GivenRunningEmulator()
        GivenRealDeviceRunning(platform="android")
        CleanupFolder('./TNS_App/platforms/android/build/outputs')
        CleanupFolder('./appTest')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        CleanupFolder('./appTest')
        CleanupFolder('./TNS_App')
        CleanupFolder('./TNS_App_NoPlatform')

    def test_001_Run_Android(self):
        output = runAUT(tnsPath + " run android --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_Run_Android_ReleaseConfiguration(self):
        output = runAUT(tnsPath + " run android --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_003_Run_Android_Default(self):
        output = runAUT(tnsPath + " run android --path TNS_App", 60)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        assert "I/ActivityManager" in output

    def test_200_Run_Android_InsideProject(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = runAUT(os.path.join("..", tnsPath) +
                        " run android --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_201_Run_Android_device_id_RenamedProjDir(self):
        runAUT("mv TNS_App appTest")
        output = runAUT(
            tnsPath +
            " run android --device emulator-5554 --path appTest --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "appTest/platforms/android/build/outputs/apk/TNSApp-debug.apk" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_300_Run_Android_PlatformNotAdded(self):
        CreateProject(projName="TNS_App_NoPlatform")
        output = runAUT(
            tnsPath +
            " run android --path TNS_App_NoPlatform --justlaunch")

        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

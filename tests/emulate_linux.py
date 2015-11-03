import os
import unittest

from helpers._os_lib import CleanupFolder, runAUT
from helpers._tns_lib import CreateProjectAndAddPlatform, androidRuntimePath, \
    tnsPath, androidKeyStorePath, androidKeyStorePassword, androidKeyStoreAlias, \
    androidKeyStoreAliasPassword, CreateProject
from helpers.device import StopEmulators, GivenRunningEmulator

# pylint: disable=R0201, C0111


class Emulate_Linux(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanupFolder('./TNSAppNoPlatform')
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

        StopEmulators()
        CleanupFolder('./TNSAppNoPlatform')
        CleanupFolder('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        StopEmulators()
        CleanupFolder('./TNS_App')

    @unittest.skip(
        "Skipped because of https://github.com/NativeScript/nativescript-cli/issues/352")
    def test_001_Emulate_Android_InRunningEmulator(self):

        GivenRunningEmulator()

        CreateProjectAndAddPlatform(
            projName="TNS_App",
            platform="android",
            frameworkPath=androidRuntimePath)
        output = runAUT(
            tnsPath +
            " emulate android --path TNS_App --timeout 600 --justlaunch",
            set_timeout=660)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output

        # Emulator can not be started without active UI
        if ('ACTIVE_UI' in os.environ) and ("YES" in os.environ['ACTIVE_UI']):
            assert "installing" in output
            assert "running" in output
            assert not "Starting Android emulator with image" in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_Emulate_Android_ReleaseConfiguration(self):

        output = runAUT(tnsPath + " emulate android --avd Api19 --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App --timeout 600 --justlaunch", set_timeout=660)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting Android emulator with image" in output
        assert "installing" in output
        assert "running" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    # TODO: Implement this test
    @unittest.skip("Not implemented.")
    def test_014_Emulate_Android_Genymotion(self):
        pass

    def test_200_Emulate_Android_InsideProjectAndSpecifyEmulatorName(self):

        currentDir = os.getcwd()
        os.chdir(os.path.join(currentDir, "TNS_App"))
        output = runAUT(
            os.path.join(
                "..",
                tnsPath) +
            " emulate android --avd Api19 --timeout 600 --justlaunch",
            set_timeout=660)
        os.chdir(currentDir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting Android emulator with image Api19" in output
        assert "installing" in output
        assert "running" in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_210_Emulate_Android_PlatformNotAdded(self):
        CreateProject(projName="TNSAppNoPlatform")
        output = runAUT(
            tnsPath +
            " emulate android --avd Api19 --timeout 600  --justlaunch --path TNSAppNoPlatform",
            set_timeout=660)
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Starting Android emulator with image Api" in output
        assert "installing" in output
        assert "running" in output

        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_401_Emulate_InvalidPlatform(self):
        output = runAUT(
            tnsPath +
            " emulate invalidPlatform --path TNS_App --timeout 600 --justlaunch",
            set_timeout=660)
        assert "The input is not valid sub-command for 'emulate' command" in output
        assert "Usage" in output

    @unittest.skip(
        "Skipped because of https://github.com/NativeScript/nativescript-cli/issues/289")
    def test_402_Emulate_InvalidAvd(self):
        output = runAUT(
            tnsPath +
            " emulate android --avd invalidDeviceId --path TNS_App --timeout 600 --justlaunch",
            set_timeout=660)
        # TODO: Modify assert when issue is fixed
        assert "'invalidPlatform' is not valid sub-command for 'emulate' command" in output
        assert "Usage" in output

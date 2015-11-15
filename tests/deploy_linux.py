'''
Test for deploy command
'''
import os
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import create_project_add_platform, ANDROID_RUNTIME_PATH, \
    TNS_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_ALIAS, \
    ANDROID_KEYSTORE_ALIAS_PASS, create_project
from helpers.device import given_running_emulator, given_real_device


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class DeployAndroid(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cleanup_folder('./TNS_App')
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_AppNoPlatform')
        given_running_emulator()
        given_real_device(platform="android")
        cleanup_folder('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cleanup_folder('./TNS_App')

    def test_001_deploy_android(self):
        output = run_aut(
            TNS_PATH +
            " deploy android --path TNS_App  --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_deploy_android_release(self):
        output = run_aut(TNS_PATH + " deploy android --keyStorePath " + ANDROID_KEYSTORE_PATH +
                        " --keyStorePassword " + ANDROID_KEYSTORE_PASS +
                        " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS +
                        " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS +
                        " --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_200_deploy_android_deviceid(self):
        output = run_aut(
            TNS_PATH +
            " deploy android --device emulator-5554 --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_201_deploy_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(os.path.join("..", TNS_PATH) +
                        " deploy android --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_300_deploy_android_platform_not_added(self):
        create_project(proj_name="TNS_AppNoPlatform")
        output = run_aut(TNS_PATH + " deploy android --path TNS_AppNoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_401_deploy_invalid_platform(self):
        output = run_aut(TNS_PATH + " deploy invalidPlatform --path TNS_App --justlaunch")
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output

    def test_402_deploy_invalid_device(self):
        output = run_aut(
            TNS_PATH +
            " deploy android --device invaliddevice_id --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Cannot resolve the specified connected device " + \
            "by the provided index or identifier" in output
        assert "To list currently connected devices and " + \
            "verify that the specified index or identifier exists, run 'tns device'" in output

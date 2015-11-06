'''
Test for deploy command
'''
import os
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import create_project_add_platform, androidRuntimePath, \
    tnsPath, androidKeyStorePath, androidKeyStorePassword, androidKeyStoreAlias, \
    androidKeyStoreAliasPassword, create_project
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
            framework_path=androidRuntimePath)

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
            tnsPath +
            " deploy android --path TNS_App  --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_deploy_android_release(self):
        output = run_aut(tnsPath + " deploy android --keyStorePath " + androidKeyStorePath +
                        " --keyStorePassword " + androidKeyStorePassword +
                        " --keyStoreAlias " + androidKeyStoreAlias +
                        " --keyStoreAliasPassword " + androidKeyStoreAliasPassword +
                        " --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_200_deploy_android_deviceid(self):
        output = run_aut(
            tnsPath +
            " deploy android --device emulator-5554 --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_201_deploy_android_insideproject(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(os.path.join("..", tnsPath) +
                        " deploy android --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_300_deploy_android_platform_not_added(self):
        create_project(proj_name="TNS_AppNoPlatform")
        output = run_aut(tnsPath + " deploy android --path TNS_AppNoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_401_deploy_invalid_platform(self):
        output = run_aut(tnsPath + " deploy invalidPlatform --path TNS_App --justlaunch")
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output

    def test_402_deploy_invalid_device(self):
        output = run_aut(
            tnsPath +
            " deploy android --device invaliddevice_id --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Cannot resolve the specified connected device " + \
            "by the provided index or identifier" in output
        assert "To list currently connected devices and " + \
            "verify that the specified index or identifier exists, run 'tns device'" in output

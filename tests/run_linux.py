'''
Tests for run command in context of Android
'''
import os
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import create_project, create_project_add_platform, \
    TNS_PATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, ANDROID_RUNTIME_PATH
from helpers.device import given_running_emulator, given_real_device


# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904
class RunAndroid(unittest.TestCase):

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

        given_running_emulator()
        given_real_device(platform="android")
        cleanup_folder('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cleanup_folder('./appTest')
        cleanup_folder('./TNS_App')
        cleanup_folder('./TNS_App_NoPlatform')

    def test_001_run_android_justlaunch(self):
        output = run_aut(TNS_PATH + " run android --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_run_android_release(self):
        output = run_aut(TNS_PATH + " run android --keyStorePath " + ANDROID_KEYSTORE_PATH +
                        " --keyStorePassword " + ANDROID_KEYSTORE_PASS +
                        " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS +
                        " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS +
                        " --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_003_run_android_default(self):
        output = run_aut(TNS_PATH + " run android --path TNS_App", 60)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        assert "I/ActivityManager" in output

    def test_200_run_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(os.path.join("..", TNS_PATH) +
                        " run android --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_201_run_android_device_id_renamed_proj_dir(self):
        run_aut("mv TNS_App appTest")
        output = run_aut(
            TNS_PATH +
            " run android --device emulator-5554 --path appTest --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "appTest/platforms/android/build/outputs/apk/TNSApp-debug.apk" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_301_run_android_patform_not_added(self):
        create_project(proj_name="TNS_App_NoPlatform")
        output = run_aut(
            TNS_PATH + " run android --path TNS_App_NoPlatform --justlaunch")

        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_302_run_android_device_not_connected(self):
        output = run_aut(TNS_PATH + " run android --device xxxxx --path TNS_App_NoPlatform")
        assert "Cannot resolve the specified connected device" in output
        assert "Project successfully prepared" not in output
        assert "Project successfully built" not in output
        assert "Successfully deployed on device" not in output

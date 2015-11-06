import os
import unittest

from helpers._os_lib import cleanup_folder, run_aut
from helpers._tns_lib import create_project, create_project_add_platform, \
    TNSPATH, ANDROID_KEYSTORE_PATH, ANDROID_KEYSTORE_PASS, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS, ANDROID_RUNTIME_PATH
from helpers.device import given_running_emulator, given_real_device

# pylint: disable=R0201, C0111


class Run_Linux(unittest.TestCase):

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
        cleanup_folder('./appTest')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cleanup_folder('./appTest')
        cleanup_folder('./TNS_App')
        cleanup_folder('./TNS_App_NoPlatform')

    def test_001_Run_Android(self):
        output = run_aut(TNSPATH + " run android --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_Run_Android_ReleaseConfiguration(self):
        output = run_aut(TNSPATH + " run android --keyStorePath " + ANDROID_KEYSTORE_PATH +
                        " --keyStorePassword " + ANDROID_KEYSTORE_PASS +
                        " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS +
                        " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS +
                        " --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_003_Run_Android_Default(self):
        output = run_aut(TNSPATH + " run android --path TNS_App", 60)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        assert "I/ActivityManager" in output

    def test_200_Run_Android_InsideProject(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run_aut(os.path.join("..", TNSPATH) +
                        " run android --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_201_Run_Android_device_id_RenamedProjDir(self):
        run_aut("mv TNS_App appTest")
        output = run_aut(
            TNSPATH +
            " run android --device emulator-5554 --path appTest --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "appTest/platforms/android/build/outputs/apk/TNSApp-debug.apk" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_300_Run_Android_PlatformNotAdded(self):
        create_project(proj_name="TNS_App_NoPlatform")
        output = run_aut(
            TNSPATH +
            " run android --path TNS_App_NoPlatform --justlaunch")

        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

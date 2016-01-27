"""
Tests for run command in context of Android
"""

import os
import unittest

from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH, ANDROID_KEYSTORE_PASS, ANDROID_KEYSTORE_PATH, \
    ANDROID_KEYSTORE_ALIAS, ANDROID_KEYSTORE_ALIAS_PASS
from core.tns.tns import Tns


class RunAndroid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Folder.cleanup('./TNS_App')
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Emulator.ensure_available()
        Device.ensure_available(platform="android")
        Folder.cleanup('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Emulator.stop_emulators()
        Folder.cleanup('./appTest')
        Folder.cleanup('./TNS_App')
        Folder.cleanup('./TNS_App_NoPlatform')

    def test_001_run_android_justlaunch(self):
        output = run(TNS_PATH + " run android --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        # TODO: Get device id and verify files are deployed and process is
        # running on this device

    def test_002_run_android_release(self):
        output = run(TNS_PATH + " run android --keyStorePath " + ANDROID_KEYSTORE_PATH +
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
        output = run(TNS_PATH + " run android --path TNS_App", 60)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        assert "I/ActivityManager" not in output  # We do not show full adb logs (only those from app)

    def test_200_run_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) +
                     " run android --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

    def test_201_run_android_device_id_renamed_proj_dir(self):
        run("mv TNS_App appTest")
        output = run(TNS_PATH + " run android --device emulator-5554 --path appTest --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output

    def test_301_run_android_patform_not_added(self):
        Tns.create_app(app_name="TNS_App_NoPlatform")
        output = run(
                TNS_PATH + " run android --path TNS_App_NoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Installing tns-android" in output
        assert "Project successfully created." in output
        # Note:
        # Do not assert that project runs because it adds latest official platform from npm,
        # it might not work with latest CLI and modules.

    def test_302_run_android_device_not_connected(self):
        output = run(TNS_PATH + " run android --device xxxxx --path TNS_App_NoPlatform --justlaunch")
        assert "Cannot resolve the specified connected device" in output
        assert "Project successfully prepared" not in output
        assert "Project successfully built" not in output
        assert "Successfully deployed on device" not in output

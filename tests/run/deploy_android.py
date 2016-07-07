"""
Test for deploy command
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


class DeployAndroid(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Folder.cleanup('./TNS_App')
        Tns.create_app_platform_add(app_name="TNS_App", platform="android", framework_path=ANDROID_RUNTIME_PATH)

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_AppNoPlatform')
        Emulator.ensure_available()
        Device.ensure_available(platform="android")
        Folder.cleanup('./TNS_App/platforms/android/build/outputs')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Folder.cleanup('./TNS_App')

    def test_001_deploy_android(self):
        output = run(TNS_PATH + " deploy android --path TNS_App  --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids(platform="android")
        for id in device_ids:
            print id
            assert id in output

    def test_002_deploy_android_release(self):
        output = run(TNS_PATH + " deploy android --keyStorePath " + ANDROID_KEYSTORE_PATH +
                     " --keyStorePassword " + ANDROID_KEYSTORE_PASS +
                     " --keyStoreAlias " + ANDROID_KEYSTORE_ALIAS +
                     " --keyStoreAliasPassword " + ANDROID_KEYSTORE_ALIAS_PASS +
                     " --release --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids("android")
        for id in device_ids:
            assert id in output

    def test_200_deploy_android_deviceid(self):
        output = run(TNS_PATH + " deploy android --device emulator-5554 --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier 'emulator-5554'" in output
        device_ids = Device.get_ids("android")
        for id in device_ids:
            assert id not in output

    def test_201_deploy_android_inside_project(self):
        current_dir = os.getcwd()
        os.chdir(os.path.join(current_dir, "TNS_App"))
        output = run(os.path.join("..", TNS_PATH) + " deploy android --path TNS_App --justlaunch")
        os.chdir(current_dir)
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids("android")
        for id in device_ids:
            assert id in output

    def test_300_deploy_android_platform_not_added(self):
        Tns.create_app(app_name="TNS_AppNoPlatform")
        output = run(TNS_PATH + " deploy android --path TNS_AppNoPlatform --justlaunch")
        assert "Copying template files..." in output
        assert "Installing tns-android" in output
        assert "Project successfully created." in output
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output

        device_ids = Device.get_ids("android")
        for id in device_ids:
            assert id in output

    def test_401_deploy_invalid_platform(self):
        output = run(TNS_PATH + " deploy invalidPlatform --path TNS_App --justlaunch")
        assert "Invalid platform invalidplatform. Valid platforms are ios or android." in output

    def test_402_deploy_invalid_device(self):
        output = run(TNS_PATH + " deploy android --device invaliddevice_id --path TNS_App --justlaunch")
        assert "Project successfully prepared" not in output
        assert "Cannot resolve the specified connected device" in output
        assert "To list currently connected devices" in output
        assert "tns device" in output

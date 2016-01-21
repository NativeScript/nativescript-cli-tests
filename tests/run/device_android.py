"""
Test for device command in context of Android
"""

import unittest
from time import sleep

from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.command import run
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH
from core.tns.tns import Tns


class DeviceAndroid(unittest.TestCase):
    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./TNS_App')
        Device.ensure_available(platform="android")
        Emulator.ensure_available()

    def tearDown(self):
        Emulator.stop_emulators()
        Folder.cleanup('./TNS_App')

    def test_001_device_list_applications_and_run_android(self):
        device_id = Device.get_id(platform="android")
        if device_id is not None:

            # Deploy TNS_App on device
            Tns.create_app_platform_add(
                    app_name="TNS_App",
                    platform="android",
                    framework_path=ANDROID_RUNTIME_PATH)
            output = run(TNS_PATH + " deploy android --path TNS_App --justlaunch")
            assert "Project successfully prepared" in output
            assert "Project successfully built" in output
            assert "Successfully deployed on device with identifier" in output
            sleep(10)

            # Verify list-applications command list org.nativescript.TNSApp
            output = run(
                    TNS_PATH +
                    " device list-applications --device " +
                    device_id)
            assert "com.android." in output
            assert "com.google." in output
            assert "org.nativescript.TNSApp" in output

            # Verify app is running
            Device.wait_until_app_is_running(app_id="org.nativescript.TNSApp",
                                             device_id=device_id, timeout=60)

            # Kill the app
            Device.stop_application(app_id="org.nativescript.TNSApp", device_id=device_id)

            # Start via emulate command and verify it is running
            run(TNS_PATH + " device emulate org.nativescript.TNSApp --device " + device_id + " --justlaunch")

            # Verify app is running
            Device.wait_until_app_is_running(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=60)

        else:
            print "Prerequisites not met. This test requires at least one real android device."
            assert False

    def test_002_device_log_android(self):
        device_id = Device.get_id("android")
        output = run(TNS_PATH + " device log --device " + device_id, timeout=60)
        assert "beginning of main" in output
        assert "beginning of system" in output
        assert "ActivityManager" in output

    def test_200_device_log_android_two_devices(self):
        if Device.get_count(platform="android") > 1:
            output = run(TNS_PATH + " device log")
            assert "More than one device found. Specify device explicitly." in output
        else:
            print "Prerequisites not met. This test requires at least two attached devices."
            assert False

    def test_400_device_invalid_platform(self):
        output = run(TNS_PATH + " device windows")
        assert "'windows' is not a valid device platform." in output
        assert "Usage" in output

    def test_401_device_log_invalid_device_id(self):
        output = run(TNS_PATH + " device log --device invaliddevice_id")
        assert "Cannot resolve the specified connected device " + \
               "by the provided index or identifier." in output

    def test_402_device_run_invalid_device_id(self):
        output = run(TNS_PATH + " device run --device invaliddevice_id")
        assert "Cannot resolve the specified connected device " + \
               "by the provided index or identifier." in output

    def test_403_device_list_applications_invalid_device_id(self):
        output = run(TNS_PATH + " device list-applications --device invaliddevice_id")
        assert "Cannot resolve the specified connected device " + \
               "by the provided index or identifier." in output

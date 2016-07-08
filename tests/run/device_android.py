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
        Device.uninstall_app(app_prefix="org.nativescript.", platform="android", fail=False)
        Emulator.ensure_available()

    def tearDown(self):
        Emulator.stop_emulators()
        Folder.cleanup('./TNS_App')

    def test_001_device_list_applications_and_run_android(self):
        device_id = Device.get_id(platform="android")
        device_ids = Device.get_ids("android")

        # Deploy TNS_App on device
        Tns.create_app_platform_add(app_name="TNS_App", platform="android", framework_path=ANDROID_RUNTIME_PATH)
        output = run(TNS_PATH + " deploy android --path TNS_App --justlaunch")
        assert "Project successfully prepared" in output
        assert "Project successfully built" in output
        assert "Successfully deployed on device with identifier" in output
        for id in device_ids:
            assert id in output
        sleep(10)

        # Verify list-applications command list org.nativescript.TNSApp
        for id in device_ids:
            output = run(TNS_PATH + " device list-applications --device " + id)
            assert "com.android." in output
            assert "org.nativescript.TNSApp" in output

        # Verify app is running
        Device.wait_until_app_is_running(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=60)

        # Get logs
        output = run(TNS_PATH + " device log --device " + device_id, timeout=60)
        assert ("ActivityManager" in output) or ("AndroidRuntime" in output) or ("Wifi" in output) or ("WIFI" in output)

        # TODO: Uncomment after https://github.com/NativeScript/nativescript-cli/issues/1912 is fixed

        # Kill the app
        #Device.stop_application(app_id="org.nativescript.TNSApp", device_id=device_id)

        # Start via emulate command and verify it is running
        #run(TNS_PATH + " device run org.nativescript.TNSApp --device " + device_id + " --justlaunch")

        # Verify app is running
        #Device.wait_until_app_is_running(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=60)

    def test_300_device_log_android_two_devices(self):
        a_count = Device.get_count(platform="android")
        i_count = Device.get_count(platform="ios")
        if a_count + i_count > 2:
            output = run(TNS_PATH + " device log")
            assert "More than one device found. Specify device explicitly." in output

    def test_400_device_invalid_platform(self):
        output = run(TNS_PATH + " device windows")
        assert "'windows' is not a valid device platform." in output

    def test_401_device_log_invalid_device_id(self):
        output = run(TNS_PATH + " device log --device invaliddevice_id")
        assert "Cannot resolve the specified connected device" in output

    @unittest.skip("Ignored because of https://github.com/NativeScript/nativescript-cli/issues/1912")
    def test_402_device_run_invalid_device_id(self):
        output = run(TNS_PATH + " device run android --device invaliddevice_id")
        assert "Cannot resolve the specified connected device" in output

    def test_403_device_list_applications_invalid_device_id(self):
        output = run(TNS_PATH + " device list-applications --device invaliddevice_id")
        assert "Cannot resolve the specified connected device" in output

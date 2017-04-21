"""
Tests for device command in context of Android
"""
import os.path
from time import sleep

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, EMULATOR_ID
from core.tns.tns import Tns
from core.settings.strings import *
from core.tns.tns_platform_type import Platform


class DeviceAndroidTests(BaseClass):

    DEVICE_ID = Device.get_id(platform=Platform.ANDROID)
    DEVICE_IDS = Device.get_ids(platform=Platform.ANDROID)

    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Folder.cleanup(cls.app_name)
        Device.ensure_available(platform=Platform.ANDROID)
        Device.uninstall_app(app_prefix="org.nativescript.", platform=Platform.ANDROID, fail=False)
        Emulator.ensure_available()

        Tns.create_app(cls.app_name, update_modules=True)
        Tns.platform_add_android(attributes={"--path": cls.app_name, "--frameworkPath": ANDROID_RUNTIME_PATH})
        cls.app_id = Tns.get_app_id(cls.app_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()
        Folder.cleanup(cls.app_name)

    def test_001_device_list(self):
        output = Tns.run_tns_command("device android")
        assert EMULATOR_ID in output
        for device_id in self.DEVICE_IDS:
            assert device_id in output

    def test_100_device_list_applications_and_run_android(self):

        # `tns deploy android` should deploy on all android devices
        output = Tns.deploy_android(attributes={"--path": self.app_name, "--justlaunch": ""})
        for device_id in self.DEVICE_IDS:
            assert device_id in output
        sleep(10)

        # Verify list-applications command list org.nativescript.TestApp
        for device_id in self.DEVICE_IDS:
            output = Tns.run_tns_command("device list-applications", attributes={"--device": self.DEVICE_ID})
            assert "com.android." in output
            assert self.app_id in output

        # Kill the app
        Device.stop_application(app_id=self.app_id, device_id=self.DEVICE_ID)
        # Start via emulate command and verify it is running
        Tns.run_tns_command("device run " + self.app_id, attributes={"--device": self.DEVICE_ID, "--justlaunch": ""},
                            timeout=60)

        # Verify app is running
        Device.wait_until_app_is_running(app_id=self.app_id, device_id=self.DEVICE_ID, timeout=20)

        # Get logs
        log = Tns.run_tns_command("device log", attributes={"--device": self.DEVICE_ID}, wait=False)
        Tns.wait_for_log(log_file=log, string_list=['beginning of'], timeout=120, clean_log=False)
        assert 'I' or 'D' or 'W' in File.read(log), "Console log does not contain INFO, DEBUG or WARN messages"

    def test_300_device_log_android_two_devices(self):
        a_count = Device.get_count(platform=Platform.ANDROID)
        i_count = Device.get_count(platform=Platform.IOS)
        if a_count + i_count > 2:
            output = Tns.run_tns_command("device log")
            assert "More than one device found. Specify device explicitly." in output

    def test_400_device_invalid_platform(self):
        output = Tns.run_tns_command("device " + invalid)
        message1 = "'{0}' is not a valid device platform.".format(invalid)
        message2 = "Unable to detect platform for which to start emulator"
        assert message1 in output or message2 in output

    def test_401_device_log_invalid_device_id(self):
        output = Tns.run_tns_command("device log", attributes={"--device": "invaliddevice_id"})
        assert cannot_resolve_device in output

    def test_402_device_run_invalid_device_id(self):
        output = Tns.run_tns_command("device run android", attributes={"--device": "invaliddevice_id"})
        assert cannot_resolve_device in output

    def test_403_device_list_applications_invalid_device_id(self):
        output = Tns.run_tns_command("device list-applications", attributes={"--device": "invaliddevice_id"})
        assert cannot_resolve_device in output

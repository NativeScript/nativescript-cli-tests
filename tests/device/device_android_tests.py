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
from core.settings.settings import ANDROID_RUNTIME_PATH
from core.tns.tns import Tns
from core.settings.strings import *


class DeviceAndroidTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Folder.cleanup(cls.app_name)
        Device.ensure_available(platform="android")
        Device.uninstall_app(app_prefix="org.nativescript.", platform="android", fail=False)
        Emulator.ensure_available()

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop()
        Folder.cleanup(cls.app_name)

    def test_001_device_list_applications_and_run_android(self):
        device_id = Device.get_id(platform="android")
        device_ids = Device.get_ids("android")

        # Deploy TNS_App on device
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        output = Tns.deploy_android(attributes={"--path": self.app_name,
                                                "--justlaunch": ""
                                                })

        for device_id in device_ids:
            assert device_id in output
        sleep(10)

        # Verify list-applications command list org.nativescript.TNSApp
        for device_id in device_ids:
            output = Tns.run_tns_command("device list-applications", attributes={"--device": device_id})
            assert "com.android." in output
            assert "org.nativescript.TNSApp" in output

        # Kill the app
        Device.stop_application(app_id="org.nativescript.TNSApp", device_id=device_id)
        # Start via emulate command and verify it is running
        Tns.run_tns_command("device run org.nativescript.TNSApp", attributes={"--device": device_id,
                                                                              "--justlaunch": ""
                                                                              },
                            timeout=60)
        # Verify app is running
        Device.wait_until_app_is_running(app_id="org.nativescript.TNSApp", device_id=device_id, timeout=20)

        # Get logs
        log = Tns.run_tns_command("device log", attributes={"--device": device_id}, wait=False)
        Tns.wait_for_log(log_file=log, string_list=['beginning of'], timeout=120, clean_log=False)
        assert 'I' or 'D' or 'W' in File.read(log), "Console log does not contain INFO, DEBUG or WARN messages"

    def test_300_device_log_android_two_devices(self):
        a_count = Device.get_count(platform="android")
        i_count = Device.get_count(platform="ios")
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

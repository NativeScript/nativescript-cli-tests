"""
Test for livesync command in context of Android devices
"""
import os
import shutil
import time
import unittest

from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, DeviceType
from core.tns.tns import Tns
from tests.livesync.livesync_helper import replace_all, verify_all_replaced


class LivesyncAndroid_Tests(unittest.TestCase):
    # LiveSync Tests on Android Device
    app_name = "TNS_App"

    @classmethod
    def setUpClass(cls):
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Device.ensure_available(platform="android")
        Device.uninstall_app(app_prefix="org.nativescript.", platform="android")

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Folder.cleanup('./' + self.app_name)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # This test executes the Run -> LiveSync
    def test_001_livesync_android_all_devices_modify_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.run_android(attributes={"--path": self.app_name})
        replace_all(app_name=self.app_name)
        Tns.livesync(platform="android", attributes={"--path": self.app_name}, log_trace=False)
        verify_all_replaced(device_type=DeviceType.ANDROID, app_name=self.app_name)

    # This test executes the Run -> LiveSync -> Run work flow on an android
    def test_002_livesync_single_device_modify_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.run_android(attributes={"--path": self.app_name})

        device_id = Device.get_id(platform="android")
        replace_all(app_name=self.app_name)
        Tns.livesync(platform="android", attributes={"--device": device_id,
                                                     "--path": self.app_name
                                                     },
                     log_trace=False)
        verify_all_replaced(device_type=DeviceType.ANDROID, app_name=self.app_name)

        File.replace(self.app_name + "/app/main-page.xml", "TEST", "RUN")
        Tns.run_android(attributes={"--path": self.app_name})
        Device.file_contains("android", self.app_name, "app/main-page.xml", text="RUN")

    def test_201_livesync_android_add_new_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.run_android(attributes={"--path": self.app_name})

        shutil.copyfile(self.app_name + "/app/main-page.xml", self.app_name + "/app/test.xml")
        shutil.copyfile(self.app_name + "/app/main-page.js", self.app_name + "/app/test.js")
        shutil.copyfile(self.app_name + "/app/app.css", self.app_name + "/app/test.css")

        os.makedirs(self.app_name + "/app/test")
        shutil.copyfile(self.app_name + "/app/main-view-model.js", self.app_name + "/app/test/main-view-model.js")

        Tns.livesync(platform="android", attributes={"--path": self.app_name})
        time.sleep(5)

        Device.file_contains("android", "TNSApp", "app/test.xml", text="TAP")
        Device.file_contains("android", "TNSApp", "app/test.js", text="page.bindingContext = ")
        Device.file_contains("android", "TNSApp", "app/test.css", text="color: #284848;")
        Device.file_contains("android", "TNSApp", "app/test/main-view-model.js", text="createViewModel()")

    @unittest.skip("TODO: Not implemented.")
    def test_202_livesync_android_delete_files(self):
        pass

    @unittest.skip("TODO: Implement this test.")
    def test_203_livesync_android_watch(self):
        pass

    def test_301_livesync_before_run(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH})
        replace_all(app_name=self.app_name)

        # Verify livesync without specify platform will sync only installed platform
        if (Device.get_count("android") > 0) and (Device.get_count("ios") > 0):
            android_id = Device.get_id(platform="android")
            ios_id = Device.get_id(platform="ios")
            print android_id
            print ios_id
            output = Tns.livesync(attributes={"--path": self.app_name})
            assert "Successfully prepared plugin tns-core-modules-widgets for ios" not in output
            assert "Project successfully prepared (ios)" not in output
            verify_all_replaced(device_type=DeviceType.ANDROID, app_name="TNSApp")
        else:
            Tns.livesync(platform="android", attributes={"--path": self.app_name}, log_trace=False)
            verify_all_replaced(device_type=DeviceType.ANDROID, app_name="TNSApp")

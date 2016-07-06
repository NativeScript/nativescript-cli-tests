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
from tests.livesync.livesync_helper import replace_all, verify_replaced, verify_all_replaced


class LiveSyncAndroid(unittest.TestCase):
    # LiveSync Tests on Android Device

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

        Folder.cleanup('./TNS_App')

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    # This test executes the Run -> LiveSync
    def test_001_livesync_android(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)
        Tns.run(platform="android", path="TNS_App")

        replace_all(app_name="TNS_App")
        Tns.livesync(platform="android", path="TNS_App")
        verify_all_replaced(device_type=DeviceType.ANDROID, app_name="TNSApp")

    # This test executes the Run -> LiveSync -> Run work flow on an android
    def test_002_livesync_run_android(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)
        Tns.run(platform="android", path="TNS_App")

        device_id = Device.get_id(platform="android")
        replace_all(app_name="TNS_App")
        Tns.livesync(platform="android", device=device_id, path="TNS_App")
        verify_all_replaced(device_type=DeviceType.ANDROID, app_name="TNSApp")

        File.replace("TNS_App/app/main-page.xml", "TEST", "RUN")
        Tns.run(platform="android", path="TNS_App")
        Device.file_contains("android", "TNSApp", "app/main-page.xml", text="RUN")

    def test_201_livesync_android_add_new_files(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)
        Tns.run(platform="android", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile(
                "TNS_App/app/main-view-model.js",
                "TNS_App/app/test/main-view-model.js")

        Tns.livesync(platform="android", path="TNS_App")
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
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)

        replace_all(app_name="TNS_App")

        # Verify livesync without specify platform prompt user to specify platform
        if (Device.get_count("android") > 0) and (Device.get_count("ios") > 0):
            print "When both android and ios are available livesync should prompt me"
            output = Tns.livesync(path="TNS_App", assert_success=False)
            assert "Multiple device platforms detected (iOS and Android). " + \
                   "Specify platform or device on command line" in output

        Tns.livesync(platform="android", path="TNS_App")
        verify_all_replaced(device_type=DeviceType.ANDROID, app_name="TNSApp")
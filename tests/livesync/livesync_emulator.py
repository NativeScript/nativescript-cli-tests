import os
import shutil
import unittest

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, DeviceType
from core.tns.tns import Tns
from tests.livesync.livesync_helper import replace_all, verify_all_replaced


class LiveSyncEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Emulator.stop_emulators()
        Simulator.stop_simulators()

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        Emulator.ensure_available()
        Folder.cleanup('TNS_App')

    def tearDown(self):
        Folder.cleanup('TNS_App')

    @classmethod
    def tearDownClass(cls):
        Emulator.stop_emulators()

    def test_001_livesync_android(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="android", framework_path=ANDROID_RUNTIME_PATH)
        Tns.run(platform="android", device="emulator-5554", path="TNS_App")
        replace_all(app_name="TNS_App")
        Tns.livesync(platform="android", emulator=True, device="emulator-5554", path="TNS_App")
        verify_all_replaced(device_type=DeviceType.EMULATOR, app_name="TNSApp")

    def test_201_livesync_android_add_files(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="android", framework_path=ANDROID_RUNTIME_PATH)
        Tns.run(platform="android", device="emulator-5554", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile("TNS_App/app/main-view-model.js", "TNS_App/app/test/main-view-model.js")
        Tns.livesync(platform="android", device="emulator-5554", path="TNS_App")

        Emulator.file_contains("TNSApp", "app/test.xml", text="TAP")
        Emulator.file_contains("TNSApp", "app/test.js", text="page.bindingContext = ")
        Emulator.file_contains("TNSApp", "app/test.css", text="color: #284848;")
        Emulator.file_contains("TNSApp", "app/test/main-view-model.js", text="createViewModel()")

    #     TODO:
    #     def test_202_livesync_android_delete_files(self):
    #         pass

    def test_301_livesync_before_run(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="android", framework_path=ANDROID_RUNTIME_PATH)
        replace_all(app_name="TNS_App")
        Tns.livesync(platform="android", emulator=True, device="emulator-5554", path="TNS_App")
        verify_all_replaced(device_type=DeviceType.EMULATOR, app_name="TNSApp")

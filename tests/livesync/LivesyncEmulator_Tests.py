import os
import shutil
import time

from core.base_class.BaseClass import BaseClass
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH, DeviceType
from core.tns.tns import Tns
from tests.livesync.livesync_helper import replace_all, verify_all_replaced


class LivesyncEmulatorTests(BaseClass):
    @classmethod
    def setUpClass(cls):
        Emulator.restart_adb()
        logfile = os.path.join("out", cls.__name__ + ".txt")
        BaseClass.setUpClass(logfile)
        Emulator.stop_emulators()
        Simulator.stop_simulators()

    def setUp(self):
        BaseClass.setUp(self)
        Emulator.ensure_available()
        Folder.cleanup(self.app_name)

    def tearDown(self):
        BaseClass.tearDown(self)
        Folder.cleanup(self.app_name)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Emulator.stop_emulators()

    def test_001_livesync_android(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.run_android(attributes={"--device": "emulator-5554",
                                    "--path": self.app_name,
                                    "--justlaunch": ""})
        replace_all(app_name=self.app_name)
        Tns.livesync(platform="android", attributes={"--emulator": "",
                                                     "--device": "emulator-5554",
                                                     "--path": self.app_name,
                                                     "--justlaunch": ""})
        time.sleep(5)
        verify_all_replaced(device_type=DeviceType.EMULATOR, app_name="TNSApp")

    def test_201_livesync_android_add_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        Tns.run_android(attributes={"--device": "emulator-5554",
                                    "--path": self.app_name,
                                    "--justlaunch": ""})

        shutil.copyfile(self.app_name + "/app/main-page.xml", self.app_name + "/app/test.xml")
        shutil.copyfile(self.app_name + "/app/main-page.js", self.app_name + "/app/test.js")
        shutil.copyfile(self.app_name + "/app/app.css", self.app_name + "/app/test.css")

        os.makedirs(self.app_name + "/app/test")
        shutil.copyfile(self.app_name + "/app/main-view-model.js", self.app_name + "/app/test/main-view-model.js")
        Tns.livesync(platform="android", attributes={"--device": "emulator-5554",
                                                     "--path": self.app_name,
                                                     "--justlaunch": ""})
        time.sleep(5)
        Emulator.file_contains("TNSApp", "app/test.xml", text="TAP")
        Emulator.file_contains("TNSApp", "app/test.js", text="page.bindingContext = ")
        Emulator.file_contains("TNSApp", "app/test.css", text="color: #284848;")
        Emulator.file_contains("TNSApp", "app/test/main-view-model.js", text="createViewModel()")

    def test_301_livesync_before_run(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_android(attributes={"--path": self.app_name,
                                             "--frameworkPath": ANDROID_RUNTIME_PATH
                                             })
        replace_all(app_name=self.app_name)
        Tns.livesync(platform="android", attributes={"--emulator": "",
                                                     "--device": "emulator-5554",
                                                     "--path": self.app_name,
                                                     "--justlaunch": ""})
        time.sleep(5)
        verify_all_replaced(device_type=DeviceType.EMULATOR, app_name="TNSApp")

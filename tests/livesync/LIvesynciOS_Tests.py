"""
Test for livesync command in context of iOS devices
"""

import os
import shutil
import unittest

from core.base_class.BaseClass import BaseClass
from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH
from core.tns.tns import Tns
import time


class LiveSynciOS(BaseClass):
    @classmethod
    def setUpClass(cls):
        BaseClass.setUpClass()
        Emulator.stop_emulators()
        Simulator.stop_simulators()

    def setUp(self):
        BaseClass.setUp(self)
        Folder.cleanup('./' + self.app_name)
        Device.ensure_available(platform="ios")
        Device.uninstall_app("org.nativescript.", platform="ios", fail=False)

    @classmethod
    def tearDownClass(cls):
        BaseClass.tearDownClass()
        Device.uninstall_app("org.nativescript.", platform="ios", fail=False)

    def test_001_livesync_ios_xml_js_css_tnsmodules_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        Tns.run_ios(attributes={"--path": self.app_name, "--justlaunch": ""})

        File.replace(self.app_name + "/app/main-page.xml", "TAP", "TEST")
        File.replace(self.app_name + "/app/main-view-model.js", "taps", "clicks")
        File.replace(self.app_name + "/app/app.css", "30", "20")

        File.replace(self.app_name + "/node_modules/tns-core-modules/LICENSE", "Copyright", "MyCopyright")
        File.replace(self.app_name + "/node_modules/tns-core-modules/application/application-common.js",
                                     "(\"globals\");", "(\"globals\"); // test")

        Tns.livesync(platform="ios", attributes={"--path": self.app_name,
                                                 "--syncAllFiles": "",
                                                 "--justlaunch": ""})
        time.sleep(5)
        Device.file_contains("ios", "TNSApp", "app/main-page.xml", text="TEST")
        Device.file_contains("ios", "TNSApp", "app/main-view-model.js", text="clicks left")
        Device.file_contains("ios", "TNSApp", "app/app.css", text="font-size: 20;")

        Device.file_contains("ios", "TNSApp", "app/tns_modules/LICENSE", text="MyCopyright")
        Device.file_contains(
                "ios",
                "TNSApp",
                "app/tns_modules/application/application-common.js",
                text="require(\"globals\"); // test")

    def test_002_livesync_ios_device(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        Tns.run_ios(attributes={"--path": self.app_name, "--justlaunch": ""})
        device_id = Device.get_id(platform="ios")
        File.replace(self.app_name + "/app/main-view-model.js", "taps", "clicks")
        Tns.livesync(platform="ios", attributes={"--path": self.app_name,
                                                 "--device": device_id,
                                                 "--justlaunch": ""})
        time.sleep(5)
        Device.file_contains("ios", "TNSApp", "app/main-view-model.js", text="clicks left")

    def test_201_livesync_ios_add_new_files(self):
        Tns.create_app(self.app_name)
        Tns.platform_add_ios(attributes={"--path": self.app_name,
                                         "--frameworkPath": IOS_RUNTIME_PATH
                                         })
        Tns.run_ios(attributes={"--path": self.app_name, "--justlaunch": ""})

        shutil.copyfile(self.app_name + "/app/main-page.xml", self.app_name + "/app/test.xml")
        shutil.copyfile(self.app_name + "/app/main-page.js", self.app_name + "/app/test.js")
        shutil.copyfile(self.app_name + "/app/app.css", self.app_name + "/app/test.css")

        os.makedirs(self.app_name + "/app/test")
        shutil.copyfile(self.app_name + "/app/main-view-model.js", self.app_name + "/app/test/main-view-model.js")

        Tns.livesync(platform="ios", attributes={"--path": self.app_name, "--justlaunch": ""})

        Device.file_contains("ios", "TNSApp", "app/test.xml", text="TAP")
        Device.file_contains("ios", "TNSApp", "app/test.js", text="page.bindingContext = ")
        Device.file_contains("ios", "TNSApp", "app/test.css", text="color: #284848;")
        Device.file_contains("ios", "TNSApp", "app/test/main-view-model.js", text="createViewModel()")

    @unittest.skip("TODO: Not implemented.")
    def test_202_livesync_ios_delete_files(self):
        pass

    @unittest.skip("TODO: Implement this test.")
    def test_203_livesync_ios_watch(self):
        pass

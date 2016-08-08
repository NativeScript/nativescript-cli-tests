"""
Test for livesync command in context of iOS devices
"""

import os
import shutil
import unittest

from core.device.device import Device
from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import IOS_RUNTIME_PATH
from core.tns.tns import Tns


class LiveSynciOS(unittest.TestCase):
    # LiveSync Tests on iOS Device

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

        Folder.cleanup('./TNS_App')
        Device.ensure_available(platform="ios")
        Device.uninstall_app("org.nativescript.", platform="ios", fail=False)

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        Device.uninstall_app("org.nativescript.", platform="ios", fail=False)

    def test_001_livesync_ios_xml_js_css_tnsmodules_files(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios", framework_path=IOS_RUNTIME_PATH)
        Tns.run(platform="ios", path="TNS_App")

        File.replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        File.replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        File.replace("TNS_App/app/app.css", "30", "20")

        File.replace("TNS_App/node_modules/tns-core-modules/LICENSE", "Copyright", "MyCopyright")
        File.replace(
                "TNS_App/node_modules/tns-core-modules/application/application-common.js",
                "(\"globals\");",
                "(\"globals\"); // test")

        Tns.livesync(platform="ios", path="TNS_App", sync_all_files=True)

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
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios", framework_path=IOS_RUNTIME_PATH)
        Tns.run(platform="ios", path="TNS_App")
        device_id = Device.get_id(platform="ios")
        File.replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        Tns.livesync(platform="ios", device=device_id, path="TNS_App")
        Device.file_contains("ios", "TNSApp", "app/main-view-model.js", text="clicks left")

    def test_201_livesync_ios_add_new_files(self):
        Tns.create_app_platform_add(app_name="TNS_App", platform="ios", framework_path=IOS_RUNTIME_PATH)
        Tns.run(platform="ios", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile("TNS_App/app/main-view-model.js", "TNS_App/app/test/main-view-model.js")

        Tns.livesync(platform="ios", path="TNS_App")

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

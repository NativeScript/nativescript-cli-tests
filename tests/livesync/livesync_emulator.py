import os
import shutil
import unittest

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.settings.settings import ANDROID_RUNTIME_PATH
from core.tns.tns import Tns


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

    def test_001_livesync_android_xml_js_css_tns_files(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)
        Tns.run(platform="android", device="emulator-5554", path="TNS_App")

        File.replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        File.replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        File.replace("TNS_App/app/app.css", "30", "20")

        File.replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        File.replace(
                "TNS_App/node_modules/tns-core-modules/application/application-common.js",
                "(\"globals\");", "(\"globals\"); // test")

        Tns.livesync(
                platform="android",
                emulator=True,
                device="emulator-5554",
                path="TNS_App")

        Emulator.app_file_contains_text("TNSApp", "app/main-page.xml", text="<Button text=\"TEST\" tap=\"{{ tapAction }}\" />")
        Emulator.app_file_contains_text("TNSApp", "app/main-view-model.js", text="this.set(\"message\", this.counter + \" clicks left\");")
        Emulator.app_file_contains_text("TNSApp", "app/app.css", text="font-size: 20;")
        Emulator.app_file_contains_text("TNSApp", "app/tns_modules/LICENSE", text="Copyright (c) 9999 Telerik AD")
        Emulator.app_file_contains_text("TNSApp", "app/tns_modules/application/application-common.js", text="require(\"globals\"); // test")

    def test_201_livesync_android_add_files(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)
        Tns.run(platform="android", device="emulator-5554", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile(
                "TNS_App/app/main-view-model.js", "TNS_App/app/test/main-view-model.js")
        Tns.livesync(
                platform="android",
                device="emulator-5554",
                path="TNS_App")

        Emulator.app_file_contains_text("TNSApp", "app/test.xml", text="<Button text=\"TAP\" tap=\"{{ tapAction }}\" />")
        Emulator.app_file_contains_text("TNSApp", "app/test.js", text="page.bindingContext = vmModule.mainViewModel;")
        Emulator.app_file_contains_text("TNSApp", "app/test.css", text="color: #284848;")
        Emulator.app_file_contains_text("TNSApp", "app/test/main-view-model.js", text="HelloWorldModel.prototype.tapAction")

    #     TODO:
    #     def test_202_livesync_android_delete_files(self):
    #         pass

    def test_301_livesync_before_run(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="android",
                framework_path=ANDROID_RUNTIME_PATH)

        File.replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        File.replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        File.replace("TNS_App/app/app.css", "30", "20")

        File.replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        File.replace(
                "TNS_App/node_modules/tns-core-modules/application/application-common.js",
                "(\"globals\");", "(\"globals\"); // test")

        Tns.livesync(
                platform="android",
                device="emulator-5554",
                path="TNS_App")

        Emulator.app_file_contains_text("TNSApp", "app/main-page.xml", text="<Button text=\"TEST\" tap=\"{{ tapAction }}\" />")
        Emulator.app_file_contains_text("TNSApp", "app/main-view-model.js", text="this.set(\"message\", this.counter + \" clicks left\");")
        Emulator.app_file_contains_text("TNSApp", "app/app.css", text="font-size: 20;")
        Emulator.app_file_contains_text("TNSApp", "app/tns_modules/LICENSE", text="Copyright (c) 9999 Telerik AD")
        Emulator.app_file_contains_text("TNSApp", "app/tns_modules/application/application-common.js", text="require(\"globals\"); // test")

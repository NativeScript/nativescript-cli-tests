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
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_PATH)
        Tns.run(platform="ios", path="TNS_App")

        File.replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        File.replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        File.replace("TNS_App/app/app.css", "30", "20")

        File.replace("TNS_App/node_modules/tns-core-modules/LICENSE", "Copyright", "MyCopyright")
        File.replace(
                "TNS_App/node_modules/tns-core-modules/application/application-common.js",
                "(\"globals\");",
                "(\"globals\"); // test")

        Tns.livesync(platform="ios", path="TNS_App")

        output = Device.cat_app_file("ios", "TNSApp", "app/main-page.xml")
        assert "TEST" in output
        output = Device.cat_app_file("ios", "TNSApp", "app/main-view-model.js")
        assert "clicks left" in output
        output = Device.cat_app_file("ios", "TNSApp", "app/app.css")
        assert "font-size: 20;" in output

        output = Device.cat_app_file("ios", "TNSApp", "app/tns_modules/LICENSE")
        assert "MyCopyright" in output
        output = Device.cat_app_file(
                "ios",
                "TNSApp",
                "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output

    def test_002_livesync_ios_device(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_PATH)
        Tns.run(platform="ios", path="TNS_App")

        device_id = Device.get_id(platform="ios")
        File.replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        Tns.livesync(platform="ios", device=device_id, path="TNS_App")

        output = Device.cat_app_file("ios", "TNSApp", "app/main-view-model.js")
        assert "clicks left" in output

    #         File.replace("TNS_App/app/main-view-model.js", "clicks", "runs")
    #         emulate(platform="ios", path="TNS_App")

    #         output = Device.cat_app_file("ios", "TNSApp", "app/main-view-model.js")
    #         assert "this.set(\"message\", this.counter + \" runs left\");" in output

    def test_201_livesync_ios_add_new_files(self):
        Tns.create_app_platform_add(
                app_name="TNS_App",
                platform="ios",
                framework_path=IOS_RUNTIME_PATH)
        Tns.run(platform="ios", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile(
                "TNS_App/app/main-view-model.js",
                "TNS_App/app/test/main-view-model.js")

        Tns.livesync(platform="ios", path="TNS_App")

        output = Device.cat_app_file("ios", "TNSApp", "app/test.xml")
        assert "TAP" in output
        output = Device.cat_app_file("ios", "TNSApp", "app/test.js")
        assert "page.bindingContext = vmModule.mainViewModel;" in output
        output = Device.cat_app_file("ios", "TNSApp", "app/test.css")
        assert "color: #284848;" in output
        output = Device.cat_app_file("ios", "TNSApp", "app/test/main-view-model.js")
        assert "HelloWorldModel.prototype.tapAction" in output

    @unittest.skip("TODO: Not implemented.")
    def test_202_livesync_ios_delete_files(self):
        pass

    @unittest.skip("TODO: Implement this test.")
    def test_203_livesync_ios_watch(self):
        pass

'''
Tests for the livesync command in context of Android emulator
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0103, C0111, R0201

import os, shutil, time, unittest

from helpers._os_lib import cat_app_file_on_emulator, cleanup_folder, replace
from helpers._tns_lib import ANDROID_RUNTIME_PATH, create_project_add_platform, run, livesync
from helpers.device import given_running_emulator, stop_emulators
from helpers.simulator import stop_simulators


class LiveSyncWindows(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # setup emulator
        stop_emulators()
        stop_simulators()

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        given_running_emulator()
        cleanup_folder('TNS_App')

    def tearDown(self):
        cleanup_folder('TNS_App')

    @classmethod
    def tearDownClass(cls):
        stop_emulators()

    def test_001_livesync_android_xml_js_css_tns_files(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        run(platform="android", device="emulator-5554", path="TNS_App")

        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");",
            "(\"globals\"); // test")

        livesync(
            platform="android",
            emulator=True,
            device="emulator-5554",
            path="TNS_App")

        output = cat_app_file_on_emulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_emulator("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        output = cat_app_file_on_emulator("TNSApp", "app/app.css")
        assert "font-size: 20;" in output

        output = cat_app_file_on_emulator("TNSApp", "app/tns_modules/LICENSE")
        assert "Copyright (c) 9999 Telerik AD" in output
        output = cat_app_file_on_emulator("TNSApp", \
            "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output

    def test_201_livesync_android_add_files(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        run(platform="android", device="emulator-5554", path="TNS_App")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test.xml")
        shutil.copyfile("TNS_App/app/main-page.js", "TNS_App/app/test.js")
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test.css")

        os.makedirs("TNS_App/app/test")
        shutil.copyfile(
            "TNS_App/app/main-view-model.js",
            "TNS_App/app/test/main-view-model.js")
        livesync(platform="android", device="emulator-5554", path="TNS_App")

        time.sleep(1)
        output = cat_app_file_on_emulator("TNSApp", "app/test.xml")
        assert "<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_emulator("TNSApp", "app/test.js")
        assert "page.bindingContext = vmModule.mainViewModel;" in output
        output = cat_app_file_on_emulator("TNSApp", "app/test.css")
        assert "color: #284848;" in output
        output = cat_app_file_on_emulator("TNSApp", "app/test/main-view-model.js")
        assert "HelloWorldModel.prototype.tapAction" in output

    def test_301_livesync_before_run(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        livesync(platform="android", device="emulator-5554", path="TNS_App")

        time.sleep(3)
        output = cat_app_file_on_emulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        
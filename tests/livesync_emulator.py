'''
Tests for livesync command in context of Android emulator
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# R0904 - Too many public methods
# pylint: disable=C0103, C0111, R0201, R0904

import os, shutil, time, unittest

from helpers._os_lib import cleanup_folder, cat_app_file_on_emulator, replace
from helpers._tns_lib import ANDROID_RUNTIME_PATH, \
    create_project_add_platform, live_sync, run
from helpers.device import given_running_emulator, stop_emulators
from helpers.simulator import stop_simulators


class LiveSyncEmulator(unittest.TestCase):

    # LiveSync Tests on Android Emulator
    # TODO: Add tests for #942

    @classmethod
    def setUpClass(cls):
        stop_emulators()
        stop_simulators()

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        cleanup_folder('./TNS_App')
        given_running_emulator()

    def tearDown(self):
        pass

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

        live_sync(
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
        live_sync(platform="android", device="emulator-5554", path="TNS_App")

        time.sleep(1)
        output = cat_app_file_on_emulator("TNSApp", "app/test.xml")
        assert "<Button text=\"TAP\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_emulator("TNSApp", "app/test.js")
        assert "page.bindingContext = vmModule.mainViewModel;" in output
        output = cat_app_file_on_emulator("TNSApp", "app/test.css")
        assert "color: #284848;" in output
        output = cat_app_file_on_emulator("TNSApp", "app/test/main-view-model.js")
        assert "HelloWorldModel.prototype.tapAction" in output

    @unittest.skip("TODO: Fix this test.")
    def test_202_livesync_android_watch(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        run(platform="android", path="TNS_App")
        replace("TNS_App/app/main-page.xml", "TAP", "TEST1")

#         print "tns livesync android --watch --path TNS_App"
#         pr = subprocess.Popen("tns livesync android --watch --path TNS_App", shell=True)
#         pr_pid = pr.pid
#
#         time.sleep(60)
#         print "assert"
#         output = cat_app_file("android", "TNSApp", "app/main-page.xml")
#         assert "<Button text=\"TEST1\" tap=\"{{ tapAction }}\" />" in output
#
#         time.sleep(5)
#         replace("TNS_App/app/main-page.xml", "TEST1", "TEST2")
#
#         time.sleep(15)
#         print "assert"
#         output = cat_app_file("android", "TNSApp", "app/main-page.xml")
#         assert "<Button text=\"TEST2\" tap=\"{{ tapAction }}\" />" in output
#
#         time.sleep(5)
#         replace("TNS_App/app/main-page.xml", "TEST2", "TEST3")
#
#         time.sleep(15)
#         print "assert"
#         output = cat_app_file("android", "TNSApp", "app/main-page.xml")
#         assert "<Button text=\"TEST3\" tap=\"{{ tapAction }}\" />" in output
#
#         print "killing child ..."
#         pr.terminate()
#
#         time.sleep(5)
#         if psutil.pid_exists(pr_pid):
#             print "force killing child ..."
#             pr.kill()

    def test_301_livesync_before_run(self):
        create_project_add_platform(
            proj_name="TNS_App",
            platform="android",
            framework_path=ANDROID_RUNTIME_PATH)
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        live_sync(platform="android", device="emulator-5554", path="TNS_App")

        time.sleep(3)
        output = cat_app_file_on_emulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

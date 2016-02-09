import shutil
import time

from core.device.emulator import Emulator
from core.device.simulator import Simulator
from core.osutils.file import File
from core.osutils.folder import Folder
from core.osutils.watcher import Watcher
from core.settings.settings import ANDROID_RUNTIME_PATH, TNS_PATH
from core.tns.tns import Tns


class LiveSyncEmulatorWatch(Watcher):
    # TODO: Add a test for #942.

    @classmethod
    def setUpClass(cls):
        # setup emulator
        Emulator.stop_emulators()
        Simulator.stop_simulators()
        Emulator.ensure_available()
        Folder.cleanup('TNS_App')
        Folder.cleanup('appTest')

        # setup app
        Tns.create_app(app_name="TNS_App", copy_from="data/apps/livesync-hello-world")
        Tns.platform_add(platform="android", framework_path=ANDROID_RUNTIME_PATH, path="TNS_App")
        Tns.run(platform="android", device="emulator-5554", path="TNS_App")

    def setUp(self):
        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.terminate_watcher()
        Emulator.stop_emulators()

        Folder.cleanup('TNS_App')
        Folder.cleanup('appTest')

    def test_001_full_livesync_android_emulator_xml_js_css_tns_files(self):
        # replace
        File.replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        File.replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        File.replace("TNS_App/app/app.css", "30", "20")

        File.replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        File.replace(
                "TNS_App/node_modules/tns-core-modules/application/application-common.js",
                "(\"globals\");", "(\"globals\"); // test")

        # livesync
        command = TNS_PATH + " livesync android --emulator --device emulator-5554 --watch --path TNS_App --log trace"
        self.start_watcher(command)
        time.sleep(10)
        self.wait_for_text_in_output("Page loaded 1 times.")

        output = Emulator.cat_app_file("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        output = Emulator.cat_app_file("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        output = Emulator.cat_app_file("TNSApp", "app/app.css")
        assert "font-size: 20;" in output

        output = Emulator.cat_app_file("TNSApp", "app/tns_modules/LICENSE")
        assert "Copyright (c) 9999 Telerik AD" in output
        output = Emulator.cat_app_file("TNSApp", "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output

    # Add new files
    def test_101_livesync_android_emulator_watch_add_xml_file(self):
        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test/test.xml")
        self.wait_for_text_in_output("Page loaded 2 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/test/test.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

    def test_102_livesync_android_emulator_watch_add_js_file(self):
        shutil.copyfile("TNS_App/app/app.js", "TNS_App/app/test/test.js")
        self.wait_for_text_in_output("Page loaded 1 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/test/test.js")
        assert "application.start();" in output

    def test_103_livesync_android_emulator_watch_add_css_file(self):
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test/test.css")
        self.wait_for_text_in_output("Page loaded 2 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/test/test.css")
        assert "color: #284848;" in output

    # Change in files
    def test_111_livesync_android_emulator_watch_change_xml_file(self):
        File.replace("TNS_App/app/main-page.xml", "TEST", "WATCH")
        self.wait_for_text_in_output("Page loaded 3 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/main-page.xml")
        assert "<Button text=\"WATCH\" tap=\"{{ tapAction }}\" />" in output

    def test_112_livesync_android_emulator_watch_change_js_file(self):
        File.replace("TNS_App/app/main-view-model.js", "clicks", "tricks")
        self.wait_for_text_in_output("Page loaded 1 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" tricks left\");" in output

    def test_113_livesync_android_emulator_watch_change_css_file(self):
        File.replace("TNS_App/app/app.css", "#284848", "green")
        self.wait_for_text_in_output("Page loaded 2 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/app.css", timeout=30)
        assert "color: green;" in output

        # Delete files

    #     def test_121_livesync_android_emulator_watch_delete_xml_file(self):
    #         remove("TNS_App/app/test/test.xml")
    #         self.wait_for_text_in_output("Page loaded 3 times.")
    #
    #         output = Emulator.cat_app_file("TNSApp", "app/test/test.xml")
    #         assert "No such file or directory" in output
    #
    #     def test_122_livesync_android_emulator_watch_delete_js_file(self):
    #         remove("TNS_App/app/test/test.js")
    #         self.wait_for_text_in_output("Page loaded 1 times.")
    #
    #         output = Emulator.cat_app_file("TNSApp", "app/test/test.js")
    #         assert "No such file or directory" in output
    #
    #     def test_123_livesync_android_emulator_watch_delete_css_file(self):
    #         remove("TNS_App/app/test/test.css")
    #         self.wait_for_text_in_output("Page loaded 2 times.")
    #
    #         output = Emulator.cat_app_file("TNSApp", "app/test/test.css")
    #         assert "No such file or directory" in output

    # Add files to a new folder
    def test_131_livesync_android_emulator_watch_add_xml_file_to_new_folder(self):
        Folder.create("TNS_App/app/folder")
        self.wait_for_text_in_output("Page loaded 1 times.", timeout=30)

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/folder/test.xml")
        self.wait_for_text_in_output("Page loaded 2 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/folder/test.xml")
        assert "<Button text=\"WATCH\" tap=\"{{ tapAction }}\" />" in output

    #         remove("TNS_App/app/folder")
    #         self.wait_for_text_in_output("app/folder/") ???
    #
    #         output = Emulator.cat_app_file("TNSApp", "app/folder/test.xml")
    #         assert "No such file or directory" in output

    def test_132_livesync_android_emulator_watch_add_js_file_to_new_folder(self):
        shutil.copyfile("TNS_App/app/app.js", "TNS_App/app/folder/test.js")
        self.wait_for_text_in_output("Page loaded 1 times.", timeout=30)
        time.sleep(2)

        output = Emulator.cat_app_file("TNSApp", "app/folder/test.js")
        assert "application.start();" in output

    def test_133_livesync_android_emulator_watch_add_css_file_to_new_folder(self):
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/folder/test.css")
        self.wait_for_text_in_output("Page loaded 2 times.", timeout=30)

        output = Emulator.cat_app_file("TNSApp", "app/folder/test.css")
        assert "color: green;" in output

        #     def test_301_livesync_android_emulator_before_run(self):
        #         self.terminate_watcher()
        #         cleanup_folder('appTest')
        #
        #         create_project_add_platform(
        #             app_name="appTest",
        #             platform="android",
        #             framework_path=ANDROID_RUNTIME_PATH)
        #
        #         # replace
        #         replace("appTest/app/main-page.xml", "TAP", "TEST")
        #         replace("appTest/app/main-view-model.js", "taps", "clicks")
        #         replace("appTest/app/app.css", "30", "20")
        #
        #         replace("appTest/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        #         replace(
        #             "appTest/node_modules/tns-core-modules/application/application-common.js",
        #             "(\"globals\");", "(\"globals\"); // test")
        #
        #         livesync(platform="android", device="emulator-5554", path="TNS_App")
        #
        #         output = Emulator.cat_app_file("TNSApp", "app/main-page.xml")
        #         assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        #         output = Emulator.cat_app_file("TNSApp", "app/main-view-model.js")
        #         assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        #         output = Emulator.cat_app_file("TNSApp", "app/app.css")
        #         assert "font-size: 20;" in output
        #
        #         output = Emulator.cat_app_file("TNSApp", "app/tns_modules/LICENSE")
        #         assert "Copyright (c) 9999 Telerik AD" in output
        #         output = Emulator.cat_app_file("TNSApp", \
        #             "app/tns_modules/application/application-common.js")
        #         assert "require(\"globals\"); // test" in output

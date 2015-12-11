'''
Tests for livesync command in context of iOS simulator
'''

# C0103 - Invalid %s name "%s"
# C0111 - Missing docstring
# R0201 - Method could be a function
# pylint: disable=C0103, C0111, R0201

import shutil, time

from helpers._os_lib import create_folder, cleanup_folder, replace, remove
from helpers._tns_lib import IOS_RUNTIME_SYMLINK_PATH, \
    create_project, platform_add, run, livesync, TNS_PATH
from helpers.device import stop_emulators
from helpers.simulator import create_simulator, delete_simulator, \
    cat_app_file_on_simulator, start_simulator, stop_simulators, \
    SIMULATOR_NAME
from helpers.watcher import Watcher


class LiveSyncSimulator(Watcher):

    @classmethod
    def setUpClass(cls):

        # setup simulator
        stop_emulators()
        stop_simulators()

        delete_simulator(SIMULATOR_NAME)
        create_simulator(SIMULATOR_NAME, 'iPhone 6s', '9.0')

        start_simulator(SIMULATOR_NAME)
        cleanup_folder('TNS_App')
        cleanup_folder('appTest')

        # setup app
        create_project(proj_name="TNS_App", copy_from="data/apps/livesync-hello-world")
        platform_add(platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, \
            path="TNS_App", symlink=True)
        run(platform="ios", emulator=True, path="TNS_App")

        # replace
        replace("TNS_App/app/main-page.xml", "TAP", "TEST")
        replace("TNS_App/app/main-view-model.js", "taps", "clicks")
        replace("TNS_App/app/app.css", "30", "20")

        replace("TNS_App/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace(
            "TNS_App/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");", "(\"globals\"); // test")

        # livesync
        command = TNS_PATH + " livesync ios --emulator --watch --path TNS_App --log trace"
        print command
        cls.start_watcher(command)

    def setUp(self):

        print ""
        print "#####"
        print self.id()
        print "#####"
        print ""

        # TODO: check is --watch still running? if not - start it again?

    def tearDown(self):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.terminate_watcher()
        stop_simulators()

        cleanup_folder('TNS_App')
        cleanup_folder('appTest')

    def test_001_full_livesync_ios_simulator_xml_js_css_tns_files(self):

        # TODO: Update with console.log() when supported on simulators ...
        self.wait_for_text_in_output("prepared")
        time.sleep(2) # ... than delete these.

        output = cat_app_file_on_simulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_simulator("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        output = cat_app_file_on_simulator("TNSApp", "app/app.css")
        assert "font-size: 20;" in output

        output = cat_app_file_on_simulator("TNSApp", "app/tns_modules/LICENSE")
        assert "Copyright (c) 9999 Telerik AD" in output
        output = cat_app_file_on_simulator("TNSApp", \
            "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output


    # Add new files
    def test_101_livesync_ios_simulator_watch_add_xml_file(self):
        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/test/test.xml")
        self.wait_for_text_in_output("app/test/test.xml to")

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output

    def test_102_livesync_ios_simulator_watch_add_js_file(self):
        shutil.copyfile("TNS_App/app/app.js", "TNS_App/app/test/test.js")
        self.wait_for_text_in_output("app/test/test.js to")
        time.sleep(2)

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.js")
        assert "application.start();" in output

    def test_103_livesync_ios_simulator_watch_add_css_file(self):
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/test/test.css")
        self.wait_for_text_in_output("app/test/test.css to")

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.css")
        assert "color: #284848;" in output


    # Change in files
    def test_111_livesync_ios_simulator_watch_change_xml_file(self):
        replace("TNS_App/app/main-page.xml", "TEST", "WATCH")
        self.wait_for_text_in_output("app/main-page.xml to")

        output = cat_app_file_on_simulator("TNSApp", "app/main-page.xml")
        assert "<Button text=\"WATCH\" tap=\"{{ tapAction }}\" />" in output

    def test_112_livesync_ios_simulator_watch_change_js_file(self):
        replace("TNS_App/app/main-view-model.js", "clicks", "tricks")
        self.wait_for_text_in_output("app/main-view-model.js to")
        time.sleep(2)

        output = cat_app_file_on_simulator("TNSApp", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" tricks left\");" in output

    def test_113_livesync_ios_simulator_watch_change_css_file(self):
        replace("TNS_App/app/app.css", "#284848", "green")
        self.wait_for_text_in_output("app/app.css to")

        output = cat_app_file_on_simulator("TNSApp", "app/app.css")
        assert "color: green;" in output


    # Delete files
    def test_121_livesync_ios_simulator_watch_delete_xml_file(self):
        remove("TNS_App/app/test/test.xml")
        self.wait_for_text_in_output("app/test/test.xml")

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.xml")
        assert "No such file or directory" in output

    def test_122_livesync_ios_simulator_watch_delete_js_file(self):
        remove("TNS_App/app/test/test.js")
        self.wait_for_text_in_output("app/test/test.js")
        time.sleep(2)

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.js")
        assert "No such file or directory" in output

    def test_123_livesync_ios_simulator_watch_delete_css_file(self):
        remove("TNS_App/app/test/test.css")
        self.wait_for_text_in_output("app/test/test.css")

        output = cat_app_file_on_simulator("TNSApp", "app/test/test.css")
        assert "No such file or directory" in output


    # Add files to a new folder
    def test_131_livesync_ios_simulator_watch_add_xml_file_to_new_folder(self):
        create_folder("TNS_App/app/folder")
        self.wait_for_text_in_output("app/folder/ to")

        shutil.copyfile("TNS_App/app/main-page.xml", "TNS_App/app/folder/test.xml")
        self.wait_for_text_in_output("app/folder/test.xml to")

        output = cat_app_file_on_simulator("TNSApp", "app/folder/test.xml")
        assert "<Button text=\"WATCH\" tap=\"{{ tapAction }}\" />" in output

#         remove("TNS_App/app/folder")
#         self.wait_for_text_in_output("app/folder/")
#
#         output = cat_app_file_on_simulator("TNSApp", "app/folder/test.xml")
#         assert "No such file or directory" in output

    def test_132_livesync_ios_simulator_watch_add_js_file_to_new_folder(self):
        shutil.copyfile("TNS_App/app/app.js", "TNS_App/app/folder/test.js")
        self.wait_for_text_in_output("app/folder/test.js to")
        time.sleep(2)

        output = cat_app_file_on_simulator("TNSApp", "app/folder/test.js")
        assert "application.start();" in output

    def test_133_livesync_ios_simulator_watch_add_css_file_to_new_folder(self):
        shutil.copyfile("TNS_App/app/app.css", "TNS_App/app/folder/test.css")
        self.wait_for_text_in_output("app/folder/test.css to")

        output = cat_app_file_on_simulator("TNSApp", "app/folder/test.css")
        assert "color: green;" in output


    def test_301_livesync_ios_simulator_before_run(self):
        self.terminate_watcher()
        cleanup_folder('appTest')

        create_project(proj_name="appTest")
        platform_add(platform="ios", framework_path=IOS_RUNTIME_SYMLINK_PATH, \
            path="appTest", symlink=True)

        # replace
        replace("appTest/app/main-page.xml", "TAP", "TEST")
        replace("appTest/app/main-view-model.js", "taps", "clicks")
        replace("appTest/app/app.css", "30", "20")

        replace("appTest/node_modules/tns-core-modules/LICENSE", "2015", "9999")
        replace(
            "appTest/node_modules/tns-core-modules/application/application-common.js",
            "(\"globals\");", "(\"globals\"); // test")

        livesync(platform="ios", emulator=True, path="appTest")

        output = cat_app_file_on_simulator("appTest", "app/main-page.xml")
        assert "<Button text=\"TEST\" tap=\"{{ tapAction }}\" />" in output
        output = cat_app_file_on_simulator("appTest", "app/main-view-model.js")
        assert "this.set(\"message\", this.counter + \" clicks left\");" in output
        output = cat_app_file_on_simulator("appTest", "app/app.css")
        assert "font-size: 20;" in output

        output = cat_app_file_on_simulator("appTest", "app/tns_modules/LICENSE")
        assert "Copyright (c) 9999 Telerik AD" in output
        output = cat_app_file_on_simulator("appTest", \
            "app/tns_modules/application/application-common.js")
        assert "require(\"globals\"); // test" in output
